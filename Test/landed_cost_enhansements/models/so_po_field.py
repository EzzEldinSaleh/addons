from odoo import api, fields, models
class Landed(models.Model):
    _inherit = "stock.landed.cost"

    sale_ids = fields.Many2many(comodel_name="sale.order", string="SOs", )
    po_ids = fields.Many2many(comodel_name="purchase.order",string="POs",)
    available_pickings = fields.Many2many(comodel_name="stock.picking", relation="hhfg", column1="gg", column2='ooj',string="Ava" )

    @api.onchange('sale_ids','po_ids','picking_ids')
    def _compute_so_doamin(self):
        for x in self:
            if x.sale_ids and x.po_ids:
                x.available_pickings = x.env['stock.picking'].search(['|', ('sale_id', 'in', x.sale_ids.ids),
                                                                    ('purchase_id', 'in', x.po_ids.ids)])
            elif x.sale_ids and not x.po_ids:
                x.available_pickings = x.env['stock.picking'].search([('sale_id', 'in', x.sale_ids.ids)])
            elif not x.sale_ids and x.po_ids:
                x.available_pickings = x.env['stock.picking'].search([('purchase_id', 'in', x.po_ids.ids)])
            else:
                x.available_pickings = x.env['stock.picking'].search([])

    @api.onchange('picking_ids')
    def onchange_purchase(self):

        list = []
        for x in self.picking_ids:
            if x.sale_id:

                list.append(x.sale_id.id)

        self.update({'sale_ids':list})
    @api.onchange('picking_ids')
    def onchange_sale(self):

        list = []
        for x in self.picking_ids:
            if x.purchase_id:
                list.append(x.purchase_id.id)

        self.update({'po_ids': list})




