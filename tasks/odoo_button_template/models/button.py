from odoo import api, fields, models
class buttoninherit(models.Model):
    _inherit = 'sale.order'

    def button_name(self):
        pass