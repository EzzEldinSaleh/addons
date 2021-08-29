""" Initialize Po Type """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class PoType(models.Model):
    """
        Initialize Po Type:
         -
    """
    _name = 'po.type'
    _description = 'Po Type'

    name = fields.Char(
        required=True,
        translate=True,
    )
    quantity_type = fields.Selection(
        [('open_quantity', 'Open Quantity'),
         ('fixed_quantity', 'Fixed Quantity')],
        default='open_quantity',
    )
    allow_validity_date = fields.Boolean()
    need_project = fields.Boolean()