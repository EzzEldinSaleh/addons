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


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    letter_credit_ids = fields.One2many(comodel_name="sale.letter.credit", inverse_name="invoice_id", )

    documentary_credit_number = fields.Char(compute='compute_letter_data')
    place_of_expiry = fields.Char(compute='compute_letter_data')
    issuing_bank = fields.Text(compute='compute_letter_data')
    corresponding_bank = fields.Text(compute='compute_letter_data')
    applicant = fields.Char(compute='compute_letter_data')
    slc_beneficiary = fields.Char(compute='compute_letter_data')
    currency_code = fields.Char(compute='compute_letter_data')
    drafts_at = fields.Char(compute='compute_letter_data')
    loading_departure = fields.Char('Port of Loading/Airport of Departure',compute='compute_letter_data')
    discharge_destination = fields.Char('Port of Discharge/Airport of Destination',compute='compute_letter_data')
    slc_description = fields.Char('Description of Goods and/or Services',compute='compute_letter_data')
    documents_required = fields.Char('Documents Required',compute='compute_letter_data')
    additional_conditions = fields.Char('Additional Conditions',compute='compute_letter_data')
    charges = fields.Char(compute='compute_letter_data')
    advise_through_bank = fields.Char("Advise Through Bank",compute='compute_letter_data')

    date_of_issue = fields.Date(string="", required=False,compute='compute_letter_data' )
    latest_date_of_shipment = fields.Date(string="", required=False,compute='compute_letter_data' )
    date_of_expiry = fields.Date(string="", required=False,compute='compute_letter_data' )

    presentation_period = fields.Char(string="Period for Presentation in Days", compute='compute_letter_data' )

    # amount = fields.Float(string="", default=0.0, required=False, )

    required_doc_ids = fields.Many2many(comodel_name="sale.letter.doc",compute='compute_letter_data')

    show_documentary_credit_number = fields.Boolean()
    show_date_and_place_of_expiry = fields.Boolean()
    show_issuing_bank = fields.Boolean()
    show_corresponding_bank = fields.Boolean()
    show_applicant = fields.Boolean()
    show_beneficiary = fields.Boolean()
    show_currency_code = fields.Boolean()
    show_drafts_at = fields.Boolean()
    show_loading_departure = fields.Boolean()
    show_discharge_destination = fields.Boolean()
    show_slc_description = fields.Boolean()
    show_documents_required = fields.Boolean()
    show_additional_conditions = fields.Boolean()
    show_charges = fields.Boolean()
    show_advise_through_bank = fields.Boolean()
    show_date_of_issue = fields.Boolean()
    show_latest_date_of_shipment = fields.Boolean()
    # show_date_of_expiry = fields.Boolean()
    show_presentation_period = fields.Boolean()
    show_required_doc_ids = fields.Boolean()
    show_partial_shipments = fields.Boolean()
    show_transhipment = fields.Boolean()
    show_slc_amount = fields.Boolean()
    show_slc_currency_id = fields.Boolean()
    show_confirmation_instructions = fields.Boolean()

    # new_field_id = fields.Many2one(comodel_name="", string="", required=False, )

    partial_shipments = fields.Selection(string="",selection=[('allowed', 'ALLOWED'), ('not_allowed', 'NOT ALLOWED') ], required=False,compute='compute_letter_data' )
    transhipment = fields.Selection(string="",selection=[('allowed', 'ALLOWED'), ('not_allowed', 'NOT ALLOWED') ], required=False,compute='compute_letter_data' )
    confirmation_instructions = fields.Selection(string="",selection=[('confirm', 'CONFIRM'), ('without', 'WITHOUT'),('may_add_confirm', 'MAY ADD CONFIRMATION'), ], required=False,compute='compute_letter_data' )
    slc_amount = fields.Float(string="", default=0.0, required=True,compute='compute_letter_data' )
    slc_currency_id = fields.Many2one(comodel_name="res.currency",compute='compute_letter_data')

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

            }

            return view_tree

    @api.depends('letter_credit_ids')
    def compute_letter_data(self):
        for rec in self:
            if rec.letter_credit_ids:
                letter = rec.letter_credit_ids[0]
                rec.documentary_credit_number = letter.documentary_credit_number
                rec.place_of_expiry = letter.place_of_expiry
                rec.issuing_bank = letter.issuing_bank
                rec.corresponding_bank = letter.corresponding_bank
                rec.applicant = letter.applicant
                rec.slc_beneficiary = letter.beneficiary
                rec.currency_code = letter.currency_code
                rec.drafts_at = letter.drafts_at
                rec.loading_departure = letter.loading_departure
                rec.discharge_destination = letter.discharge_destination
                rec.slc_description = letter.description
                rec.documents_required = letter.documents_required
                rec.additional_conditions = letter.additional_conditions
                rec.charges = letter.charges
                rec.advise_through_bank = letter.advise_through_bank
                rec.date_of_issue = letter.date_of_issue
                rec.date_of_expiry = letter.date_of_expiry
                rec.presentation_period = letter.presentation_period
                rec.partial_shipments = letter.partial_shipments
                rec.transhipment = letter.transhipment
                rec.slc_amount = letter.amount
                rec.slc_currency_id = letter.currency_id.id
                rec.required_doc_ids = letter.required_doc_ids.ids
                rec.latest_date_of_shipment = letter.latest_date_of_shipment
                rec.confirmation_instructions = letter.confirmation_instructions
