""" Initialize Account Move """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         -
    """
    _inherit = 'account.move'

    sale_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        compute='_compute_sale_id'
    )

    blanket_order_id = fields.Many2one(
        "sale.blanket.order",
        string="Origin blanket order",
        related="sale_id.blanket_order_id",
    )
    project_id = fields.Many2one(
        'project',
        related='blanket_order_id.project_id',
        store=1
    )
    po_type_id = fields.Many2one(
        'po.type',
        related='blanket_order_id.po_type_id',
        store=1
    )

    @api.depends('invoice_origin')
    def _compute_sale_id(self):
        """ Compute sale_id value """
        for rec in self:
            if rec.invoice_origin:
                if rec.invoice_origin.startswith('S'):
                    rec.sale_id = self.env['sale.order'].search([('name', '=', rec.invoice_origin)], limit=1)
                else:
                    rec.sale_id = None
            else:
                rec.sale_id =None


