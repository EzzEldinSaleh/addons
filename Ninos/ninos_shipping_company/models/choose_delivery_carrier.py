""" Initialize Choose Delivery Carrier """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class ChooseDeliveryCarrier(models.TransientModel):
    """
        Inherit Choose Delivery Carrier:
         - 
    """
    _inherit = 'choose.delivery.carrier'

    shipping_company_id = fields.Many2one(
        'shipping.company',
        related='carrier_id.shipping_company_id'
    )