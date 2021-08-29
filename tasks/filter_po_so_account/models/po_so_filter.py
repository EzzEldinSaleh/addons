from odoo import api, fields, models
class PoFilter(models.Model):





    _inherit = 'account.move'
    
    partner_ids = fields.Many2many(comodel_name="res.partner", required=False, compute='_compute_partner_rank')
    @api.depends('move_type')
    def _compute_partner_rank(self):
        for x in self:
            if x.move_type in ['out_invoice','out_refund','out_receipt']:
            
                rank_search=x.env['res.partner'].search([('customer_rank', '>', 0)])
            elif x.move_type in ['in_invoice','in_refund','in_receipt']:
            
                rank_search=x.env['res.partner'].search([('supplier_rank', '>', 0)])
            else:
                rank_search=x.env['res.partner'].search([])
            x.partner_ids=rank_search.ids
            


       
