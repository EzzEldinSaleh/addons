from odoo import api, fields, models
import logging
class report(models.AbstractModel):
    _name = 'report.report.ezz_report'

    @api.model
    def _get_report_values(self, docids, data=None):

            # get the report action back as we will need its data
        report = self.env['ir.actions.report']._get_report_from_name('report.ezz_report')

        # for i in data['form']['customer_ids']:
        partner_ids = data['form']['customer_ids']
        domain = [('order_id.partner_id', 'in', partner_ids), ('order_id.date_order', '>=', data['form']['date_from']),
             ('order_id.date_order', '<=', data['form']['date_to'])]
        if data['form']['product_ids']:
            domain.append(('product_id','in', data['form']['product_ids'] ))
        sale_order_lines = self.env['sale.order.line'].search(domain)

        # partner = self.env['res.partner'].search(
        #     [('id', '=', i)])
        data = {}
        for line in sale_order_lines:
            partner_id = line.order_id.partner_id.id
            if str(partner_id) not in data:
                data[str(partner_id)] = {
                    'name': line.order_id.partner_id.name,
                    'num_products': 1,
                    'products': {str(line.product_id.id): [line.product_id.name, line.price_subtotal]}
                }
            else:
                product_id = line.product_id.id
                if str(product_id) not in data[str(partner_id)]['products']:
                    if line.product_id:

                        data[str(partner_id)]['products'][str(product_id)] = [line.product_id.name, line.price_subtotal]
                        data[str(partner_id)]['num_products'] += 1
                else:
                    data[str(partner_id)]['products'][str(product_id)][1] += line.price_subtotal


        return {
            'doc_model': 'sale.wizard',
            'data':data,
        }


