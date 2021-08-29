from odoo import api, fields, models
class hrpenalty(models.Model):
    _name = 'hr.penalty'
    _rec_name = 'name'
    name = fields.Many2one('hr.employee',"Employee")
    date = fields.Date(string="Date", required=False, )
    amount = fields.Float(string="Amount",  required=False, )
    note = fields.Text(string="Note", required=False, )
    state = fields.Selection(string="state",default='draft', selection=[('draft', 'Draft'), ('confirm', 'Confirm'),('done','Done') ], required=False, )
    def button_con(self):
        self.state='confirm'

    def button_don(self):
        self.state = 'done'
    def button_set_draftt(self):
        self.state = 'draft'