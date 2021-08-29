""" Initialize Sale Order """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         -
    """
    _inherit = 'sale.order'

    shipping_company_id = fields.Many2one(
        'shipping.company',
        related='carrier_id.shipping_company_id',
        store=1
    )
