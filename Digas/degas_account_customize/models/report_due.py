# -*- coding: utf-8 -*-
#############################################################################


from datetime import datetime, date, timedelta
from odoo.exceptions import UserError, Warning


import time
from odoo import models, fields, api
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo.tools.translate import _
from odoo.tools import append_content_to_html, DEFAULT_SERVER_DATE_FORMAT, html2plaintext



class AccountMove(models.AbstractModel):
    _inherit = 'account.followup.report'

    def _get_columns_name(self, options):
        """
        Override
        Return the name of the columns of the follow-ups report
        """
        headers = [{ 'style': 'width:30%;'},
                   {'name': _('Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap; width:10%;'},
                   {'name': _('Due Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap; width:10%;'},
                   {'name': _('Source  Document'), 'style': 'text-align:center; white-space:nowrap;width:5%;'},
                   {'name': _('Picking'), 'style': 'text-align:center; white-space:nowrap; width:10%;'},
                   {'name': _('Po.NO'), 'style': 'text-align:center; white-space:nowrap;width:5%;'},
                   {'name': _('Remarks'), 'style': 'text-align:center; white-space:nowrap; width:10%;'},
                   {'name': _('Excluded'), 'class': 'date', 'style': 'white-space:nowrap; width:10%;'},
                   {'name': _('Total Due'), 'class': 'number o_price_total', 'style': 'text-align:right; white-space:nowrap; width:10%;'}
                   ]
        if self.env.context.get('print_mode'):
            headers = headers[:7] + headers[8:]  # Remove the 'Expected Date' and 'Excluded' columns
        return headers

    def _get_lines(self, options, line_id=None):
        """
        Override
        Compute and return the lines of the columns of the follow-ups report.
        """
        # Get date format for the lang
        partner = options.get('partner_id') and self.env['res.partner'].browse(options['partner_id']) or False
        if not partner:
            return []

        lang_code = partner.lang if self._context.get('print_mode') else self.env.user.lang or get_lang(self.env).code
        lines = []
        res = {}
        today = fields.Date.today()
        line_num = 0
        for l in partner.unreconciled_aml_ids.filtered(lambda l: l.company_id == self.env.company):
            if l.company_id == self.env.company:
                if self.env.context.get('print_mode') and l.blocked:
                    continue
                currency = l.currency_id or l.company_id.currency_id
                if currency not in res:
                    res[currency] = []
                res[currency].append(l)
        for currency, aml_recs in res.items():
            total = 0
            total_issued = 0
            for aml in aml_recs:
                amount = aml.amount_residual_currency if aml.currency_id else aml.amount_residual
                date_due = format_date(self.env, aml.date_maturity or aml.date, lang_code=lang_code)
                total += not aml.blocked and amount or 0
                is_overdue = today > aml.date_maturity if aml.date_maturity else today > aml.date
                is_payment = aml.payment_id
                if is_overdue or is_payment:
                    total_issued += not aml.blocked and amount or 0
                if is_overdue:
                    date_due = {'name': date_due, 'class': 'color-red date', 'style': 'white-space:nowrap;text-align:center;color: red;'}
                if is_payment:
                    date_due = ''
                po_no = aml.move_id.ref or ''
                payment_sate = dict(aml.move_id._fields['payment_state'].selection).get(aml.move_id.payment_state)
                print("** payment_sate ==> ", payment_sate)
                remarks = payment_sate or ''
                invoice_origin = aml.move_id.invoice_origin or ''
                picking = aml.move_id.picking
                if len(invoice_origin) > 43:
                    invoice_origin = invoice_origin[:40] + '...'
                if self.env.context.get('print_mode'):
                    po_no = {'name': po_no, 'style': 'text-align:center; white-space:normal;  width:5%;'}
                    remarks = {'name': remarks, 'style': 'text-align:center; white-space:normal; width:10%'}
                    invoice_origin = {'name': invoice_origin, 'style': 'text-align:center; white-space:normal; width:5%'}
                amount = formatLang(self.env, amount, currency_obj=currency)
                line_num += 1


                columns = [
                    format_date(self.env, aml.date, lang_code=lang_code),
                    date_due,
                    invoice_origin,
                    picking,
                    po_no,
                    remarks,
                    {'name': '', 'blocked': aml.blocked},
                    amount,
                    ]
                if self.env.context.get('print_mode'):
                    print("*** col")
                    columns = columns[:6] + columns[7:]
                lines.append({
                    'id': aml.id,
                    'account_move': aml.move_id,
                    'name': aml.move_id.name,
                    'caret_options': 'followup',
                    'move_id': aml.move_id.id,
                    'type': is_payment and 'payment' or 'unreconciled_aml',
                    'unfoldable': False,
                    'columns': [type(v) == dict and v or {'name': v} for v in columns],
                })
            total_due = formatLang(self.env, total, currency_obj=currency)
            line_num += 1
            lines.append({
                'id': line_num,
                'name': '',
                'class': 'total',
                'style': 'border-top-style: double',
                'unfoldable': False,
                'level': 3,
                'columns': [{'name': v} for v in [''] * (5 if self.env.context.get('print_mode') else 6) + [total >= 0 and _('Total Due') or '', total_due]],
            })
            if total_issued > 0:
                total_issued = formatLang(self.env, total_issued, currency_obj=currency)
                line_num += 1
                lines.append({
                    'id': line_num,
                    'name': '',
                    'class': 'total',
                    'unfoldable': False,
                    'level': 3,
                    'columns': [{'name': v} for v in [''] * (5 if self.env.context.get('print_mode') else 6) + [_('Total Overdue'), total_issued]],
                })
            # Add an empty line after the total to make a space between two currencies
            line_num += 1
            lines.append({
                'id': line_num,
                'name': '',
                'class': '',
                'style': 'border-bottom-style: none',
                'unfoldable': False,
                'level': 0,
                'columns': [{} for col in columns],
            })
        # Remove the last empty line
        if lines:
            lines.pop()
        return lines
