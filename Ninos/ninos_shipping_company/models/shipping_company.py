""" Initialize Shipping Company """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class ShippingCompany(models.Model):
    """
        Initialize Shipping Company:
         - 
    """
    _name = 'shipping.company'
    _description = 'Shipping Company'
    _sql_constraints = [
        ('unique_name', 
         'UNIQUE(name)', 
         'Name must be unique'),
    ]
    
    name = fields.Char(
        required=True,
        translate=True,
    )