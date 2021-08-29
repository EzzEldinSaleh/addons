from odoo import api, fields, models
class saleorderinherit(models.Model):
    _inherit = 'sale.order'

    dis_type = fields.Selection(string="Dis Type", selection=[('per', 'Percent'), ('f', 'Fixed'), ], required=False, )
    amount_dis = fields.Float(string="Dis Amount",  required=False, )
    amount = fields.Float(string="Dis%",  readonly=True )

    @api.onchange('amount_dis','dis_type')
    def onchange_distype(self):
        if self.dis_type:
            if self.dis_type == 'per':
                amount=(self.amount_dis/100)*self.amount_untaxed
                self.amount=amount
                self.amount_total=(self.amount_untaxed-self.amount)+self.amount_tax

                if self.amount_dis > 100:
                    self.amount_dis=100

            if self.dis_type == 'f':
                self.amount = self.amount_dis
                self.amount_total=(self.amount_untaxed-self.amount)+self.amount_tax
