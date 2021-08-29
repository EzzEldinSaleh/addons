# -*- coding: utf-8 -*-
""" Account Invoice Reports """

from num2words import num2words
from odoo import api, fields, models


class Invoice(models.Model):
    _inherit = 'account.move'

    performa_invoice_no = fields.Char()
    bl_no = fields.Char(string="BL No.")
    port_of_loading = fields.Char()
    port_of_discharge = fields.Char(related='partner_id.port_discharge')
    lc_nu_date = fields.Char(string="LC Number and Date")
    documentary_credit = fields.Char(string="Documentary Credit Issuing Bank")
    beneficiary = fields.Many2one(
        comodel_name="res.partner",
        string="Beneficiary/Shipper",
    )

    to_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="To Partner",
    )
    beneficiary_bank_id = fields.Many2one(
        'account.journal', string="Beneficiary's Bank Details",
        domain=[('type', '=', 'bank'), ('use_in_invoice', '=', True)],
    )
    terms_and_conditions_id = fields.Many2one(
        comodel_name="base.terms.and.conditions",
    )
    delivery_country_id = fields.Many2one('res.country', string='Place Of Delivery Country', ondelete='restrict')
    delivery_state_id = fields.Many2one("res.country.state", string='Place Of Delivery State', ondelete='restrict',
                               domain="[('country_id', '=?', delivery_country_id)]")

    amount_in_words = fields.Char(compute="_compute_amount_in_words", store=True)
    terms_and_conditions = fields.Text()
    carrier = fields.Char()
    carying_vessel = fields.Char()
    date_of_shipment = fields.Date()
    mode_of_shipment = fields.Char()

    freight_per_mt = fields.Monetary(string="Freight Per MT", currency_field='currency_id')
    freight_charge = fields.Monetary(compute="_compute_freight_charge", currency_field='currency_id')
    commodity_price = fields.Monetary(compute="_compute_commodity_price", currency_field='currency_id')
    nu_bags = fields.Char(string="Total no. of Bags",)

    @api.multi
    @api.depends('amount_total', 'freight_per_mt')
    def _compute_freight_charge(self):
        for record in self:
            total_qty = sum(record.invoice_line_ids.mapped('quantity'))
            record.freight_charge = total_qty * record.freight_per_mt

    @api.multi
    @api.depends('amount_total', 'freight_charge')
    def _compute_commodity_price(self):
        for record in self:
            record.commodity_price = record.amount_total - record.freight_charge

    @api.multi
    @api.depends('amount_total', 'company_id.currency_id')
    def _compute_amount_in_words(self):
        for record in self:
            currency = record.currency_id
            if currency:
                amount_in_words = currency.amount_to_text(record.amount_total)
                record.amount_in_words = amount_in_words and amount_in_words.title()


class InvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    container = fields.Char()
    net_weight = fields.Float()
    gross_weight = fields.Float()
