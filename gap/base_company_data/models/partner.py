# -*- coding: utf-8 -*-
""" Add Partner Data """

from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    po_box = fields.Char(string="po.box")
