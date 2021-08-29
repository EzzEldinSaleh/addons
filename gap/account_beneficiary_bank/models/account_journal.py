# -*- coding: utf-8 -*-
""" Commercial Account Invoice Bank """

from odoo import fields, models


class Journal(models.Model):
    _inherit = 'account.journal'

    country_id = fields.Many2one(
        comodel_name='res.country',
        ondelete='restrict',
    )
    state_id = fields.Many2one(
        comodel_name="res.country.state",
        ondelete='restrict',
        domain="[('country_id', '=?', country_id)]",
    )
    street = fields.Char()
    po_box = fields.Char(
        string="Po.Box",
    )
    phone = fields.Char()
    use_in_invoice = fields.Boolean()
    iban = fields.Char(
        string="IBAN",
    )
    swft = fields.Char(
        string="SWFT",
    )
