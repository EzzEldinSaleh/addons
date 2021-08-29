""" Initialize Rental Pricing """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class RentalPricing(models.Model):
    """
        Initialize Rental Pricing:
         -
    """
    _name = 'ben.rental.pricing'
    _description = 'Rental Pricing'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    model_id = fields.Many2one(
        'product.category'
    )
    name = fields.Char(
        related='model_id.name',
        translate=True,
    )
    warehouse_ids = fields.Many2many(
        'stock.warehouse'
    )
    all_warehouse_ids = fields.Many2many(
        'stock.warehouse',
        compute='_compute_all_warehouse_ids'
    )
    km_free = fields.Float(
        default=300
    )
    # pricing_ids = fields.One2many(
    #     'pricing.pricing',
    #     'rental_pricing_id'
    # )
    km_extra_cost = fields.Float()
    km_open = fields.Float()
    fuel = fields.Float()
    hour = fields.Float()
    month = fields.Float()
    week = fields.Float()
    day = fields.Float()
    normal_insurance = fields.Float()
    general_insurance = fields.Float()
    franchise_insurance = fields.Float()
    fine_separation_counter = fields.Float()
    late_return_ids = fields.One2many(
        'late.return',
        'rental_pricing_id'
    )
    difference_return_ids = fields.One2many(
        'difference.return',
        'rental_pricing_id'
    )

    @api.depends('warehouse_ids')
    def _compute_all_warehouse_ids(self):
        """ Compute all_warehouse_ids value """
        for rec in self:
            if rec.warehouse_ids:
                rec.all_warehouse_ids = rec.warehouse_ids
            else:
                rec.all_warehouse_ids = self.env['stock.warehouse'].search([])


class PricingPricing(models.Model):
    """
        Initialize Pricing Pricing:
         - 
    """
    _name = 'pricing.pricing'
    _description = 'Pricing Pricing'
    
    uom_id = fields.Many2one(
        'uom.uom', 
        string='Unit Of Measure'
    )
    price = fields.Float()
    rental_pricing_id = fields.Many2one(
        'ben.rental.pricing'
    )


class LateReturn(models.Model):
    """
        Initialize Late Return:
         -
    """
    _name = 'late.return'
    _description = 'Late In Return'

    condition = fields.Selection(
        [('between', 'Between'),
         ('bigger_than', 'Bigger Than')],
        default='between',
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit Of Measure'
    )
    late_from = fields.Integer(
        'From'
    )
    to = fields.Integer()
    amount = fields.Float()
    rental_pricing_id = fields.Many2one(
        'ben.rental.pricing'
    )


class DifferenceReturn(models.Model):
    """
        Initialize Difference Return:
         -
    """
    _name = 'difference.return'
    _description = 'Difference Time Return'

    condition = fields.Selection(
        [('between', 'Between'),
         ('bigger_than', 'Bigger Than')],
        default='between',
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit Of Measure'
    )
    late_from = fields.Integer(
        'From'
    )
    to = fields.Integer()
    amount = fields.Float()
    rental_pricing_id = fields.Many2one(
        'ben.rental.pricing'
    )
