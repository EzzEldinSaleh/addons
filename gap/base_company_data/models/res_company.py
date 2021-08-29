# -*- coding: utf-8 -*-
""" Add Company Data """

from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    fax = fields.Char()
    name_ar = fields.Char()
    po_box = fields.Char(string="po.box")
