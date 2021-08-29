# -*- coding: utf-8 -*-
#############################################################################


from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning




class AccountMove(models.Model):
    _inherit = 'account.move'

    picking = fields.Char(string="Picking#", required=False, compute="get_picking",)
    delivery_count = fields.Integer(string='Delivery Orders', compute='get_picking')



    @api.depends('move_type','invoice_origin')
    def get_picking(self):
        for rec in self:
            if rec.move_type =='out_invoice' and rec.invoice_origin:
                picking = rec.env['stock.picking'].search([('origin','=',rec.invoice_origin)],order='name')
                ref = ''
                for res in picking:
                    if ref == '' :
                        ref = res.name
                    else:
                        ref =ref +', '+ res.name

                rec.picking = ref
                rec.delivery_count = len(picking)
            else:
                rec.picking=False
                rec.delivery_count=0

        pass
    def action_view_delivery(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")

        pickings  = self.env['stock.picking'].search([('origin','=',self.invoice_origin)])
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == 'outgoing')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        return action





