""" Initialize Product Product """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class ProductProduct(models.Model):
    """
        Inherit Product Product:
         -
    """
    _inherit = 'product.template'

    has_translate = fields.Char('Has Translation', compute='_compute_has_translate',)

    def _compute_has_translate(self):
        for rec in self:
            locale = self._context.get('lang')
            # or 'en_US'
            if locale == 'en_US':
                trans = self.env['ir.translation'].search([('src', '=', rec.name),('value', '!=', rec.name),('value', '!=', '')])
                print("trans == ",trans)
                if trans:
                    value = trans[0].value
                    desc = value
                    rec.description = desc
                    rec.has_translate = desc
                else:
                    rec.has_translate = rec.name

            if locale == 'ar_001' or locale == 'ar_SY':
                trans = self.env['ir.translation'].search([('value', '=', rec.name),('src', '!=', rec.name),('src', '!=', '')])
                print("trans == ",trans)
                if trans:
                    value = trans[0].src
                    desc = value
                    rec.description = desc
                    rec.has_translate = desc
                else:
                    rec.has_translate = rec.name



