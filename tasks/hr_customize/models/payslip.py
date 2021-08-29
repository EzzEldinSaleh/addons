from odoo import api, fields, models
class payslipin(models.Model):
    _inherit = 'hr.payslip'

    amount_pen = fields.Float(string="Amount",  required=False, compute="_compute_amount_pen")
    amount_aw = fields.Float(string="Amount",  required=False, compute="_compute_amount_awa")
    amount_tra = fields.Float(string="Amount",  required=False, compute="_compute_amount_travel")
    @api.depends()
    def _compute_amount_pen(self):
        for s in self:

            penalties=s.env["hr.penalty"].search([('date','>=',s.date_from),('date','<=',s.date_to),('name','=',s.employee_id.id)])
            amount=0
            for x in penalties:
                amount=amount+x.amount
            if amount>0:
                s.amount_pen=-amount
            else:
                s.amount_pen=0
    @api.depends()
    def _compute_amount_travel(self):
        for s in self:

            travels=s.env["hr.travel"].search([('date_from', '>=', s.date_from), ('date_to', '<=', s.date_to), ('employee_id', '=', s.employee_id.id)])
            amount=sum(travels.mapped('amount'))


            if amount>0:
                s.amount_tra=amount
            else:
                s.amount_tra=0
    @api.depends()
    def _compute_amount_awa(self):
        for s in self:

            awards=s.env["hr.award"].search([('date','>=',s.date_from),('date','<=',s.date_to),('name','=',s.employee_id.id)])
            amount=0
            for x in awards:
                amount=amount+x.amount
            if amount > 0:
                s.amount_aw=amount
            else:
                s.amount_aw=0