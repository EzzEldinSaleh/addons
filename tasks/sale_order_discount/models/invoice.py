from odoo import api, fields, models
class saleorderinherit(models.Model):
    _inherit = 'account.move'

    dis_type = fields.Selection(string="Dis Type", selection=[('per', 'Percent'), ('f', 'Fixed'), ], required=False, )
    amount_dis = fields.Float(string="Dis Amount",  required=False, )
    amount = fields.Float(string="Dis%",  readonly=True )

