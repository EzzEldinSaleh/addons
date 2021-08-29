""" Initialize Stock Picking """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class StockPicking(models.Model):
    """
        Inherit Stock Picking:
         -
    """
    _inherit = 'stock.picking'

    shipping_company_id = fields.Many2one(
        'shipping.company',
        related='carrier_id.shipping_company_id'
    )