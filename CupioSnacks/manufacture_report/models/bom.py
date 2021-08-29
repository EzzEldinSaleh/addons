""" Initialize  Init """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class MrpBomLine(models.Model):
    """
        Inherit Mrp Bom Line:
         -
    """
    _inherit = 'mrp.bom.line'

    to_consume = fields.Float(
        compute='_compute_to_consume'
    )
    fp = fields.Integer(
        compute='_compute_fp'
    )

    @api.depends('product_qty', 'bom_id')
    def _compute_to_consume(self):
        """ Compute to_consume value """
        for rec in self:
            if rec.product_qty:
                if rec.bom_id.product_qty > 0:
                    rec.to_consume = rec.product_qty / rec.bom_id.product_qty
                else:
                    rec.to_consume = 0
            else:
                rec.to_consume = 0

    @api.depends('to_consume', 'product_id')
    def _compute_fp(self):
        """ Compute fp value """
        for rec in self:
            if rec.product_id:
                if rec.to_consume > 0:
                    rec.fp = rec.product_id.qty_available / rec.to_consume
                else:
                    rec.fp = 0
            else:
                rec.fp = 0
