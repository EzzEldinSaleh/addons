# -*- coding: utf-8 -*-
""" Terms And Conditions Model"""

from odoo import fields, models


class TermsAndConditions(models.Model):
    _name = 'base.terms.and.conditions'

    name = fields.Text('Terms And Conditions')
