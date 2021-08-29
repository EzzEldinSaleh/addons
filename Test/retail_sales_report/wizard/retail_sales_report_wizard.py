# -*- coding: utf-8 -*-
""" init object """
import pytz
import base64
import io
from io import BytesIO
from psycopg2.extensions import AsIs
from babel.dates import format_date, format_datetime, format_time
from odoo import fields, models, api, _ ,tools, SUPERUSER_ID
from odoo.exceptions import ValidationError,UserError
from datetime import datetime , date ,timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from dateutil.relativedelta import relativedelta
from odoo.fields import Datetime as fieldsDatetime
import calendar
from odoo import http
from odoo.http import request
from odoo import tools

import logging
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

LOGGER = logging.getLogger(__name__)


class RetailSalesWizard(models.TransientModel):
    _name = 'retail.sales.report.wizard'
    _description = 'retail.sales.report.wizard'

    def default_date_from(self):
        today = fieldsDatetime.now()
        return today.replace(hour=0,minute=0,second=0)

    def default_date_to(self):
        today = fieldsDatetime.now()
        return today.replace(hour=23,minute=59,second=59)

    date_from = fields.Datetime(required=True,default=lambda self:self.default_date_from())
    date_to = fields.Datetime(required=True,default=lambda self:self.default_date_to())
    type = fields.Selection(string="Report Type",default="xls", selection=[('xls', 'XLS'), ('pdf', 'PDF'), ], required=True, )
    product_ids = fields.Many2many(comodel_name="product.product",string="Products")
    product_tag_ids = fields.Many2many(comodel_name="product.tag", string="Product Tags", )
    branch_ids = fields.Many2many(comodel_name="pos.branch", string="Branches", )
    season_ids = fields.Many2many(comodel_name="product.season", string="Seasons", )
    categ_ids = fields.Many2many(comodel_name="product.category", string="Product Categories", )
    user_ids = fields.Many2many(comodel_name="hr.employee", string="Sales Person", )
    cashier_ids = fields.Many2many('hr.employee', 'cashier_rel', 'cashier_id', 'cashier_id2',string="Cashiers", )
    vendor_ids = fields.Many2many(comodel_name="res.partner", string="Vendors", )
    vendor_type = fields.Selection(selection=[('consignment', 'Consignment'), ('cash', 'Cash'), ], required=False, )
    excel_sheet = fields.Binary('Download Report')
    excel_sheet_name = fields.Char(string='Name', size=64)

    def get_taxes_line(self,line):
        fpos = line.order_id.fiscal_position_id
        tax_ids_after_fiscal_position = fpos.map_tax(line.tax_ids, line.product_id, line.order_id.partner_id) if fpos else line.tax_ids
        price = line.product_id.lst_price or line.product_id.sale_price
        taxes = tax_ids_after_fiscal_position.compute_all(price, line.order_id.pricelist_id.currency_id, 1, product=line.product_id, partner=line.order_id.partner_id)
        return taxes['total_excluded']

    def get_branch_id(self,key):
        return str(eval(key)[0])

    def convert_date_to_local(self,dat, tz):
        local = tz and pytz.timezone(tz) or pytz.timezone('UTC')
        dat = dat.replace(tzinfo=pytz.utc)
        dat = dat.astimezone(local)
        dat.strftime('%Y-%m-%d: %H:%M:%S')
        return dat.replace(tzinfo=None)

    def get_report_data(self):
        data = {}
        totals = {}
        totals_dic = {
            'qty': 0,
            'total_sales': 0,
            'discount': 0,
            'price_subtotal_incl': 0,
            'price_subtotal': 0,
            'tax_amount': 0,
            'total_cost': 0,
        }
        totals.setdefault('all_total', totals_dic.copy())
        if self.date_from and self.date_to and self.date_from >= self.date_to:
            raise ValidationError(_('Date from must be before date to!'))
        end_date = self.date_to
        # end_time = datetime.max.time()
        # end_date = datetime.combine(end_date, end_time)

        products = self.env['product.product'].sudo().search(['|',('active','=',True),('active','=',False)])
        if self.vendor_ids:
            # vendor_product_info = self.env['product.supplierinfo'].sudo().search([('name','in',self.vendor_ids.ids)])
            # products = products.filtered(lambda p:p.variant_seller_ids in vendor_product_info)
            vendor_nums = self.vendor_ids.mapped('id')
            # if type(vendor_nums) is not list:
            #     vendor_nums = list(vendor_nums)
            products = products.filtered(lambda p:p.partner_vendor_id.id in vendor_nums)

        elif self.vendor_type:
            # vendor_product_info = self.env['product.supplierinfo'].sudo().search([('name.vendor_type','=',self.vendor_type)])
            # products = products.filtered(lambda p:p.variant_seller_ids in vendor_product_info)
            vendor_nums = self.env['res.partner'].sudo().search([('vendor_type','=',self.vendor_type)]).mapped('id')
            if type(vendor_nums) is not list:
                vendor_nums = list(vendor_nums)
            products = products.filtered(lambda p:p.partner_vendor_id.id in vendor_nums)

        if self.product_ids:
            products = products & self.product_ids

        elif self.product_tag_ids:
            products = products.filtered(lambda p: p.product_tag_ids in self.product_tag_ids)

        elif self.categ_ids:
            categories = self.env['product.category'].sudo().search([('id', 'child_of', self.categ_ids.ids)])
            products = products.filtered(lambda p: p.categ_id in categories)

        if self.season_ids:
            products = products.filtered(lambda p: p.season_id in self.season_ids)

        branch_ids = self.env['pos.branch'].sudo().search([]).ids
        if self.branch_ids:
            branch_ids = self.branch_ids.ids

        order_domain = [
            ('date_order', '>=', self.date_from),
            ('date_order', '<=', str(end_date)),
            ('session_id.config_id.pos_branch_id', 'in', branch_ids),
        ]

        if self.user_ids:
            order_domain.append(('sale_person_id','in',self.user_ids.ids))

        if self.cashier_ids:
            order_domain.append(('employee_id','in',self.cashier_ids.ids))

        pos_orders = self.env['pos.order'].sudo().search(order_domain)
        order_lines = self.env['pos.order.line'].sudo().search([
            ('order_id','in',pos_orders.ids),
            ('product_id','in',products.ids),
        ])
        ref_partner_dict = {}
        for ol in order_lines:
            branch = ol.order_id.session_id.config_id.pos_branch_id
            product = ol.product_id
            # variant_seller_id = product.variant_seller_ids and product.variant_seller_ids[0] or self.env['product.supplierinfo']
            # partner = variant_seller_id.name

            if product.partner_vendor_id not in ref_partner_dict:
                partner = self.env['res.partner'].sudo().search([('id','=',product.partner_vendor_id.id)],limit=1)
                ref_partner_dict[product.partner_vendor_id.name] = partner
            partner = ref_partner_dict[product.partner_vendor_id.name]
            user = ol.order_id.sale_person_id
            cashier = ol.order_id.employee_id
            # key = (branch.id,user.id,product.id)
            key = (branch.id,ol.id,user.id,cashier.id)
            date_order = self.convert_date_to_local(ol.order_id.date_order,self.env.user.tz)
            sale_price = ol.original_price or product.lst_price or product.sale_price
            product_data = {
                'partner':partner.name or '',
                'vendor_type':partner.vendor_type or '',
                'branch':branch.name,
                'categ':product.categ_id.name,
                'barcode':product.barcode,
                'default_code':product.default_code,
                'date_order': datetime.strftime(date_order,'%d/%m/%Y: %H:%M:%S'),
                'product':product.display_name,
                'order_name':ol.order_id.name,
                'season':product.season_id.name,
                'qty':0,
                'sales_price': sale_price,
                'total_sales':0,
                'discount':0,
                'price_subtotal_incl':0,
                'price_subtotal':0,
                'cost':product.standard_price,
                'total_cost':0,
                'tax_amount':0,
                'sale_person':ol.order_id.sale_person_id.name,
                'cashier':ol.order_id.employee_id.name,
            }

            data.setdefault(key,product_data.copy())
            totals.setdefault(branch.id,totals_dic.copy())
            total_sales = sale_price * ol.qty
            total_discount = total_sales - ol.price_subtotal_incl
            tax_amount = ol.price_subtotal_incl - ol.price_subtotal
            price_subtotal_incl = ol.price_subtotal_incl
            price_subtotal = ol.price_subtotal
            data[key]['qty'] += ol.qty
            data[key]['total_sales'] += total_sales
            data[key]['discount'] += total_discount
            data[key]['price_subtotal_incl'] += price_subtotal_incl
            data[key]['price_subtotal'] += price_subtotal
            data[key]['tax_amount'] += tax_amount
            data[key]['total_cost'] += product.standard_price * ol.qty

            totals[branch.id]['qty'] += ol.qty
            totals[branch.id]['total_sales'] += total_sales
            totals[branch.id]['discount'] += total_discount
            totals[branch.id]['price_subtotal_incl'] += price_subtotal_incl
            totals[branch.id]['price_subtotal'] += price_subtotal
            totals[branch.id]['tax_amount'] += tax_amount
            totals[branch.id]['total_cost'] += product.standard_price * ol.qty

            totals['all_total']['qty'] += ol.qty
            totals['all_total']['total_sales'] += total_sales
            totals['all_total']['discount'] += total_discount
            totals['all_total']['price_subtotal_incl'] += price_subtotal_incl
            totals['all_total']['price_subtotal'] += price_subtotal
            totals['all_total']['tax_amount'] += tax_amount
            totals['all_total']['total_cost'] += product.standard_price * ol.qty

        return data,totals,branch_ids

    def action_print_excel_file(self):
        self.ensure_one()
        data,totals,branch_ids = self.get_report_data()
        print("data ==>",data)
        print("totals ==>",totals)
        print("branch_ids ==>",branch_ids)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        TABLE_HEADER = workbook.add_format({
            'bold': 1,
            'font_name': 'Tahoma',
            'border': 0,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
        })

        header_format = workbook.add_format({
            'bold': 1,
            'font_name': 'Aharoni',
            'border': 0,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
            'bg_color': '#c3c6c5',
        })

        TABLE_HEADER_Data = TABLE_HEADER
        TABLE_HEADER_Data.num_format_str = '#,##0.00_);(#,##0.00)'
        STYLE_LINE = workbook.add_format({
            'border': 0,
            'align': 'center',
            'valign': 'vcenter',
        })

        TABLE_data = workbook.add_format({
            'bold': 1,
            'font_name': 'Aharoni',
            'border': 0,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
        })
        TABLE_data.num_format_str = '#,##0.00'
        TABLE_data_tolal_line = workbook.add_format({
            'bold': 1,
            'font_name': 'Aharoni',
            'border': 1,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
            'bg_color': 'yellow',
        })

        TABLE_data_tolal_line.num_format_str = '#,##0.00'
        TABLE_data_o = workbook.add_format({
            'bold': 1,
            'font_name': 'Aharoni',
            'border': 0,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
        })
        STYLE_LINE_Data = STYLE_LINE
        STYLE_LINE_Data.num_format_str = '#,##0.00_);(#,##0.00)'

        worksheet = workbook.add_worksheet('تقرير مبيعات مورد')
        lang = self.env.user.lang
        worksheet.right_to_left()

        row = 0
        col = 0
        worksheet.merge_range(row, row, col, col + 3, _('تقرير مبيعات مورد'), STYLE_LINE_Data)
        row += 1
        worksheet.write(row, col, _('التاريخ من'), STYLE_LINE_Data)
        col += 1
        worksheet.write(row, col, str(self.date_from), STYLE_LINE_Data)
        col += 1
        worksheet.write(row, col, _('التاريخ الى'), STYLE_LINE_Data)
        col += 1
        worksheet.write(row, col, str(self.date_to), STYLE_LINE_Data)
        row += 2

        col = 0
        worksheet.write(row, col, _('اسم المورد'), header_format)
        col += 1
        worksheet.write(row, col, _('نوع المورد'), header_format)
        col += 1
        worksheet.write(row, col, _('اسم الفرع'), header_format)
        col += 1
        worksheet.write(row, col, _('تصنيف المنتج'), header_format)
        col += 1
        worksheet.write(row, col, _('باركود المنتج'), header_format)
        col += 1
        worksheet.write(row, col, _('اسم المنتج'), header_format)
        col += 1
        worksheet.write(row, col, _('الموديل'), header_format)
        col += 1
        worksheet.write(row, col, _('الموسم'), header_format)
        col += 1
        worksheet.write(row, col, _('رقم ايصال البيع'), header_format)
        col += 1
        worksheet.write(row, col, _('تاريخ الايصال'), header_format)
        col += 1
        worksheet.write(row, col, _('اجمالي كمية المبيعات'), header_format)
        col += 1
        worksheet.write(row, col, _('سعر البيع'), header_format)
        col += 1
        worksheet.write(row, col, _('اجمالي المبيعات'), header_format)
        col += 1
        worksheet.write(row, col, _('التخفيضات'), header_format)
        col += 1
        worksheet.write(row, col, _('صافي المبيعات (غير شامل الضرائب)'), header_format)
        col += 1
        worksheet.write(row, col, _('اجمالي قيمة الضرائب'), header_format)
        col += 1
        worksheet.write(row, col, _('صافي المبيعات (شامل الضرائب)'), header_format)
        col += 1
        worksheet.write(row, col, _('قيمة التكلفة'), header_format)
        col += 1
        worksheet.write(row, col, _('اجمالي التكلفة'), header_format)
        col += 1
        worksheet.write(row, col, _('الكاشير'), header_format)
        col += 1
        worksheet.write(row, col, _('البائع'), header_format)
        sorted_keys = sorted(data.keys())
        previous_branch = sorted_keys and sorted_keys[0][0] or -1
        print("previous_branch ==> ",previous_branch)
        print("sorted_keys ==> ",sorted_keys)
        for i,key in enumerate(sorted_keys):
            row += 1
            branch_id = key[0]
            if branch_id != previous_branch:
                worksheet.write(row, 10, totals[previous_branch]['qty'], TABLE_data_tolal_line)
                worksheet.write(row, 12, totals[previous_branch]['total_sales'], TABLE_data_tolal_line)
                worksheet.write(row, 14, totals[previous_branch]['price_subtotal'], TABLE_data_tolal_line)
                worksheet.write(row, 15, totals[previous_branch]['tax_amount'], TABLE_data_tolal_line)
                worksheet.write(row, 16, totals[previous_branch]['price_subtotal_incl'], TABLE_data_tolal_line)
                worksheet.write(row, 18, totals[previous_branch]['total_cost'], TABLE_data_tolal_line)
                row += 1
                previous_branch = branch_id

            col = 0
            worksheet.write(row, col, data[key]['partner'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['vendor_type'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['branch'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['categ'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['barcode'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['product'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['default_code'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['season'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['order_name'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['date_order'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['qty'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['sales_price'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['total_sales'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['discount'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['price_subtotal'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['tax_amount'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['price_subtotal_incl'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['cost'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['total_cost'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['cashier'], STYLE_LINE_Data)
            col += 1
            worksheet.write(row, col, data[key]['sale_person'], STYLE_LINE_Data)

            if i == len(sorted_keys) -1:
                row += 1
                worksheet.write(row, 10, totals[branch_id]['qty'], TABLE_data_tolal_line)
                worksheet.write(row, 12, totals[branch_id]['total_sales'], TABLE_data_tolal_line)
                worksheet.write(row, 14, totals[branch_id]['price_subtotal'], TABLE_data_tolal_line)
                worksheet.write(row, 15, totals[branch_id]['tax_amount'], TABLE_data_tolal_line)
                worksheet.write(row, 16, totals[branch_id]['price_subtotal_incl'], TABLE_data_tolal_line)
                worksheet.write(row, 18, totals[branch_id]['total_cost'], TABLE_data_tolal_line)

        row += 1
        worksheet.merge_range('A' + str(row) + ':I' + str(row), _('الاجمالي'), TABLE_data_tolal_line)
        worksheet.write(row,10, totals['all_total']['qty'], TABLE_data_tolal_line)
        worksheet.write(row, 12, totals['all_total']['total_sales'], TABLE_data_tolal_line)
        worksheet.write(row, 14, totals['all_total']['price_subtotal'], TABLE_data_tolal_line)
        worksheet.write(row, 15, totals['all_total']['tax_amount'], TABLE_data_tolal_line)
        worksheet.write(row, 16, totals['all_total']['price_subtotal_incl'], TABLE_data_tolal_line)
        worksheet.write(row, 18, totals['all_total']['total_cost'], TABLE_data_tolal_line)

        if data:
            self.excel_sheet_name = 'تقرير مبيعات مورد'
            workbook.close()
            output.seek(0)
            self.excel_sheet = base64.encodestring(output.read())
            self.excel_sheet_name = str(self.excel_sheet_name) + '.xlsx'
            return {
                'type': 'ir.actions.act_url',
                'name': '41 Report',
                'url': '/web/content/retail.sales.report.wizard/%s/excel_sheet/تقرير مبيعات مورد.xlsx?download=true' % (self.id),
                'target': 'self'
            }

        else:

            view_action = {
                'name': _(' Retail Sales Report'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'retail.sales.report.wizard',
                'type': 'ir.actions.act_window',
                'res_id': self.id,
                'target': 'new',
                'context': self.env.context,
            }

            return view_action

    def action_print_pdf(self):
        data,totals,branch_ids = self.get_report_data()
        new_data = {}
        totals_data = {}
        for key in totals:
            new_key = str(key)
            totals_data[new_key] = totals[key]

        for key in data:
            new_key = str(key)
            new_data[new_key] = data[key]

        result={
            'docs':self,
            'docids':self.ids,
            'data':new_data,
            'totals': totals_data,
            'keys': sorted(new_data.keys()),
            'branch_ids': branch_ids,
            'date_from':self.date_from,
            'date_to':self.date_to,
        }
        return self.env.ref('retail_sales_report.retail_sales_report').report_action(docids=self.ids, data=result)



    def action_print(self):
        print("self.type == > ",self.type )
        if self.type == 'xls':

            return self.action_print_excel_file()

        elif self.type == 'pdf':
            return self.action_print_pdf()

