""" Initialize Delivery Carrier """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class DeliveryCarrier(models.Model):
    """
        Inherit Delivery Carrier:
         - 
    """
    _inherit = 'delivery.carrier'
    
    shipping_company_id = fields.Many2one(
        'shipping.company'
    )
