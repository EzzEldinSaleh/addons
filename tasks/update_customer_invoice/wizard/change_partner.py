""" Initialize Change Partner """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class ChangePartner(models.TransientModel):
    """
        Initialize Change Partner:
         -
    """
    _name = 'change.partner'
    _description = 'Change Partner'

    def _default_invoices(self):
        invoices = self.env.context.get('active_ids', [])
        return invoices
    invoice_ids = fields.Many2many(
        'account.move',
        default=_default_invoices
    )
    partner_id = fields.Many2one(
        'res.partner'
    )

    def change_partner(self):
        """ Change Partner """
        for rec in self:
            for inv in rec.invoice_ids:
                if inv.state == 'draft':
                    inv.update({
                        'partner_id': rec.partner_id.id
                    })
