# -*- coding: utf-8 -*-
""" init object """
from odoo import fields, models, api, _ ,tools, SUPERUSER_ID
from odoo.exceptions import ValidationError,UserError
from datetime import datetime , date ,timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from dateutil.relativedelta import relativedelta
from odoo.fields import Datetime as fieldsDatetime
import calendar
from odoo import http
from odoo.http import request
from odoo import tools
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare

import logging

LOGGER = logging.getLogger(__name__)


class SaleLetterCredit(models.Model):
    _name = 'sale.letter.credit'
    _rec_name = 'name'
    _description = 'Letter Of Credit'
    _inherit = ['mail.thread']

    name = fields.Char(string="Name", )
    date = fields.Date(default=fields.Date.today(), )
    # expiration_date = fields.Date(default=fields.Date.today(), )
    country_id = fields.Many2one(comodel_name="res.country")
    partner_id = fields.Many2one(comodel_name="res.partner",string="Customer")
    currency_id = fields.Many2one(comodel_name="res.currency",default= lambda  self:self.env.user.company_id.currency_id.id)
    currency_rate = fields.Float()

    documentary_credit_number = fields.Char()
    place_of_expiry = fields.Char()
    issuing_bank = fields.Text()
    corresponding_bank = fields.Text()
    applicant = fields.Char()
    beneficiary = fields.Char()
    currency_code = fields.Char()
    drafts_at = fields.Char()
    loading_departure = fields.Char('Port of Loading/Airport of Departure')
    discharge_destination = fields.Char('Port of Discharge/Airport of Destination')
    description = fields.Char('Description of Goods and/or Services')
    documents_required = fields.Char('Documents Required')
    additional_conditions = fields.Char('Additional Conditions')
    charges = fields.Char()
    advise_through_bank = fields.Char("Advise Through Bank")

    date_of_issue = fields.Date(string="", default=lambda self: fields.Date.today(), required=False, )
    latest_date_of_shipment = fields.Date(string="", default=lambda self: fields.Date.today(), required=False, )
    date_of_expiry = fields.Date(string="", default=lambda self: fields.Date.today(), required=False, )

    presentation_period = fields.Char(string="Period for Presentation in Days", )

    # amount = fields.Float(string="", default=0.0, required=False, )

    required_doc_ids = fields.Many2many(comodel_name="sale.letter.doc",)

    # new_field_id = fields.Many2one(comodel_name="", string="", required=False, )

    partial_shipments = fields.Selection(string="",selection=[('allowed', 'ALLOWED'), ('not_allowed', 'NOT ALLOWED') ], required=False, )
    transhipment = fields.Selection(string="",selection=[('allowed', 'ALLOWED'), ('not_allowed', 'NOT ALLOWED') ], required=False, )
    confirmation_instructions = fields.Selection(string="",selection=[('confirm', 'CONFIRM'), ('without', 'WITHOUT'),('may_add_confirm', 'MAY ADD CONFIRMATION'), ], required=False, )

    sale_id = fields.Many2one(
        comodel_name='sale.order',
        string='Add Sale Order',domain=[('state','in',[('pi','lc_ack','so_draft','lc_confirm')])],copy=False,
    )
    invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        domain="[('id','in',invoice_ids),('letter_credit_ids','=',False)]"
    )
    invoice_ids = fields.Many2many(
        related='sale_id.invoice_ids',copy=False,
    )

    charging_type = fields.Selection(default="partial", selection=[('partial', 'Partial'), ('whole', 'Whole'), ], )
    payment_term_id = fields.Many2one(comodel_name="account.payment.term", )
    incoterm_id = fields.Many2one('account.incoterms', 'Incoterm',
            help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    delivery_date = fields.Date(default=fields.Date.today(), )
    user_id = fields.Many2one(comodel_name="res.users", string="Responsible Person", )
    # bank_id = fields.Many2one(comodel_name="res.bank" )
    beneficiary_bank_id = fields.Many2one(
        'account.journal', string="Beneficiary's Bank Details",
        domain=[('type', '=', 'bank'), ('use_in_invoice', '=', True)],
    )
    type_of_lc = fields.Many2one(comodel_name="sale.letter.credit.type", string="LC Type", )

    state = fields.Selection(string="Status",default="draft", selection=[('draft', 'Draft'), ('acknowledged', 'Acknowledged'), ('confirmed', 'Confirmed') ], required=False, )
    customs_clearance_number = fields.Char()
    document_ids = fields.One2many(comodel_name="sale.letter.credit.attachment", inverse_name="letter_credit_id", string="Documents", required=False, )
    amount = fields.Float(string="", default=0.0, required=True, )

    # @api.model
    # def create(self, values):
    #     res = super(SaleLetterCredit, self).create(values)
    #     if res.invoice_id:
    #         res.invoice_id.write({'sale_letter_credit_id': res.id})
    #     return res

    @api.onchange('sale_id')
    def sale_order_change(self):
        if not self.sale_id:
            return {}
        if not self.partner_id:
            self.partner_id = self.sale_id.partner_id.id
        self.payment_term_id = self.sale_id.payment_term_id
        self.env.context = dict(self.env.context, from_sale_order_change=True)
        # self.sale_id = False
        return {}

    @api.model
    def create(self, values):
        """
        Override create to add sequence.
        :param values:
        """
        # values['name'] = self.env['ir.sequence'].next_by_code('sale.letter.credit') or ' '
        if 'currency_id' in values:
            currency = self.env['res.currency'].browse(values.get('currency_id'))
            values['currency_rate'] = currency.rate
        res = super(SaleLetterCredit, self).create(values)
        return res

    @api.onchange('currency_id')
    def onchange_currency(self):
        self.update({'currency_rate': self.currency_id.rate})

    @api.onchange('sale_id')
    def onchange_sale_id(self):
        self.update({'invoice_id': None})

    def action_ack(self):
        if not self.documentary_credit_number:
            raise ValidationError(_('Documentary Credit Number is required'))

        if not self.place_of_expiry:
            raise ValidationError(_('Place Of Expiry is required'))

        if not self.advise_through_bank:
            raise ValidationError(_('Advise Through Bank is required'))

        if not self.date_of_issue:
            raise ValidationError(_('Date Of Issue is required'))

        if not self.issuing_bank:
            raise ValidationError(_('Issuing Bank is required'))

        if not self.corresponding_bank:
            raise ValidationError(_('Corresponding Bank is required'))

        if not self.date_of_expiry:
            raise ValidationError(_('Date Of Expiry is required'))

        self.write({'state': 'acknowledged'})
        if self.sale_id.state in ['pi']:
            self.sale_id.write({'state':'lc_ack'})

    def action_confirm(self):
        self.write({'state': 'confirmed'})
        if self.sale_id.state in ['lc_ack','so_draft']:
            self.sale_id.write({'state':'lc_confirm'})


class SaleLetterCreditType(models.Model):
    _name = 'sale.letter.credit.type'

    name = fields.Char()


class SaleLetterDoc(models.Model):
    _name = 'sale.letter.doc'

    name = fields.Char(required=True)



