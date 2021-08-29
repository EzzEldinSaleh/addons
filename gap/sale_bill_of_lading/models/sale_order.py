# -*- coding: utf-8 -*-
""" Sale Bill Of Lading"""

from odoo import api, fields, models

import logging

LOGGER = logging.getLogger(__name__)


class Order(models.Model):

    _inherit = 'sale.order'

    bill_of_lading_ids = fields.One2many(
        comodel_name='sale.bill.of.lading',
        inverse_name="order_id",
    )
    bill_of_lading = fields.Char()
    bl_count = fields.Integer(compute='_compute_number_of_bl')

    @api.depends('bill_of_lading_ids')
    @api.multi
    def _compute_number_of_bl(self):
        for record in self:
            record.bl_count = record.bill_of_lading_ids and len(record.bill_of_lading_ids)
