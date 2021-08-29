# -*- coding: utf-8 -*-
""" init object """
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

LOGGER = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    letter_credit_ids = fields.One2many(comodel_name="sale.letter.credit", inverse_name="sale_id", )
    letter_credit_count = fields.Integer(compute='compute_letter_credit_count')
    need_lc = fields.Boolean(default=False  )
    pi_status = fields.Selection(string="PI Status",default="",
                                 selection=[('new', 'New'),
                                            ('pipeline', 'Pipeline'),
                                            ('payment in transit', 'Payment In Transit'),
                                            ('waiting action', 'Waiting Action'),
                                            ('done', 'Done'),
                                            ('cancelled', 'Cancelled'),
                                            ],
                                 required=False, )

    def action_open_lc(self):
        for one in self:

            domain = [('id', 'in', one.letter_credit_ids.ids)]
            view_tree = {
                'name': _(' Letter Of Credit '),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.letter.credit',
                'type': 'ir.actions.act_window',
                'domain': domain,
                'context': {'default_partner_id': one.partner_id.id,'default_sale_id': one.id},

            }

            return view_tree

    def action_draft_so(self):
        self.write({'state':'so_draft'})

    @api.multi
    def action_confirm(self):
        if self.need_lc:
            if not self.letter_credit_ids.filtered(lambda l:l.state in ['confirmed']):
                raise ValidationError(_('You can not confirm the SO unless at least one LC is confirmed'))
        return super(SaleOrder,self).action_confirm()

    @api.multi
    def action_convert_to_pi(self):
        if not self.need_lc:
            return super(SaleOrder,self).action_convert_to_pi()
        else:
            if self.letter_credit_ids.filtered(lambda l:l.state in ['confirmed']):
                self.write({'state':'lc_confirm'})
            elif self.letter_credit_ids.filtered(lambda l:l.state in ['confirmed']):
                self.wirte({'state':'lc_ack'})
            else:
                return super(SaleOrder, self).action_convert_to_pi()

    def compute_letter_credit_count(self):
        for rec in self:
            rec.letter_credit_count = len(rec.letter_credit_ids)
