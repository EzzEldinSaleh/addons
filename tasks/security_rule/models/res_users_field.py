from odoo import api, fields, models
class usersinherit(models.Model):
    _inherit = 'res.users'
    analytic_account_default_ids = fields.Many2many(comodel_name="account.analytic.account",  relation="geg", column1="rr", column2="gg",string="Account Analytic Default", )
    analytic_tags_default_ids = fields.Many2many(comodel_name="account.analytic.tag", relation="y", column1="b", column2="f", string="Account Tags Default", )