from odoo import api, fields, models
class wizardchange(models.TransientModel):
    _name = 'wizard.change'



    invoice_ids = fields.Many2many(
        'account.move',
    )

    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, )
    def change_partner(self):
        ids=self.env.context.get('active_ids', [])
        for x in ids:
            x.partner_id=self.partner_id.id
        return