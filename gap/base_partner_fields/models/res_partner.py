from odoo import api, fields, models,_
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    commercial = fields.Char(string="Commercial Registry", required=False, )
    fax = fields.Char(string="Fax", required=False, )
    port_discharge = fields.Char(string="Port of discharge", required=False, )


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    swift_code = fields.Char(string="Swift Code", required=False, )
