from odoo import api, fields, models
class serverinvoice(models.Model):

    _inherit = 'account.move'

    def namejjv(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': "wizard.change",
            'view_mode': "form",
            'target': 'new',
        }