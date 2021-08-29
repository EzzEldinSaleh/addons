from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError
class hrtravel(models.Model):
    _name = 'hr.travel'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee','Employee')
    date_from = fields.Date(string="Date From", required=True, )
    date_to = fields.Date(string="Date To", required=True, )
    amount = fields.Float(string="Amount",  required=False, compute='compute_amount')
    duration = fields.Integer(string="Duration", required=False, compute='compute_duration')
    travel_type = fields.Selection(string="Travel Type", selection=[('int', 'internal'), ('ab', 'abroad'), ], required=False, )
    @api.depends()
    def compute_duration(self):
        for rec in  self:

            if rec.date_from and rec.date_to:
                d1 = datetime.strptime(str(rec.date_from), '%Y-%m-%d')
                d2 = datetime.strptime(str(rec.date_to), "%Y-%m-%d")
                rec.duration= abs((d1 - d2).days)

    @api.constrains('date_from','date_to')
    def compute_month(self):

        if self.date_from.month != self.date_to.month:
            raise ValidationError("you cant make travel within tow monthes")

    @api.depends()
    def compute_amount(self):
        for rec in self:
            search=self.env['hr.contract'].search([('employee_id','=',self.employee_id.id),('state','=','open')])

            if rec.travel_type:
                if rec.travel_type == 'int':
                    amount=search.int_allow*rec.duration
                if rec.travel_type == 'ab':
                    amount=search.abd_allow*rec.duration
                rec.amount =amount
            else:
                rec.amount=0
class contractin(models.Model):
    _inherit = 'hr.contract'

    int_allow = fields.Integer(string="Internal Allow", required=False, )
    abd_allow = fields.Integer(string="Abroad Allow", required=False, )


































































