from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class Loans(models.Model):
    _name = 'loan'
    _inherit = ['mail.thread','mail.activity.mixin']
    name = fields.Char("Name" , tracking=True)
    total = fields.Integer("Loan Amount")
    state = fields.Selection(string="state",default='d', selection=[('d', 'Draft'), ('co', 'Confirm'),('do', 'Done') ,('c', 'Cancel')], required=False, )
    num_of_loan = fields.Integer("Number Of Loans")
    date = fields.Date(string="First Loan", required=True,default=fields.Date.today() )
    pay = fields.Integer(string="Pay After", required=False, )
    num_invoices = fields.Integer(string="Payment", required=False,compute="_compute_num")
    d_or_m_or_y = fields.Selection(string="D M Y", selection=[('d','Day'),('m', 'Month'), ('y', 'Year'), ], required=True, )
    loan_amount = fields.Float("Loan Amount" ,)
    first_amount = fields.Float("First Loan Amount" ,)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, tracking=True)
    loans_ids = fields.One2many(comodel_name="loan.line", inverse_name="loan_id", string="loan", required=False, readonly=True)


    # @api.depends()


    def action_confirm(self):
        self.state='co'
    def action_cancel(self):
        self.state = 'c'

    def action_create_invoice(self):

        for x in self.loans_ids:
            if x.payment_id:
                if x.payment_id.state == 'draft':
                    raise ValidationError('Last installment not paid')
            else:
                if x.is_paid == False:



                    vals={
                    'payment_type':'outbound',
                    'partner_type':'customer',
                    # 'name':self.name,
                    # 'partner_id':self.partner_id.id,
                    'date':x.date,
                    'amount':x.amount
                }

                    x.is_paid=True

                    create=self.env['account.payment'].create(vals)
                    x.payment_id=create.id


                break
    def action_set_draft(self):
        self.state = 'd'
    @api.depends()
    def _compute_num(self):
        payments = self.loans_ids.mapped('payment_id')
        num_paymentss=self.env['account.payment'].search_count([('id', 'in', payments.ids)])
        self.num_invoices=num_paymentss



    def invoice_num(self):
        payments=self.loans_ids.mapped('payment_id')


        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'domain': [('id', 'in', payments.ids)],

        }

    def action_create_loanline(self):
        for loan in self:
            loan.loans_ids.unlink()
            date_start = loan.date

            if self.total and self.num_of_loan:
                total = self.total - self.first_amount
                num = self.num_of_loan - 1
                amount = total / num
            else:
                amount = 0

            for i in range(1, loan.num_of_loan + 1):
                if i == 1:
                    self.env['loan.line'].create({
                        'amount': loan.first_amount,
                        'number': i,
                        'date': date_start,
                        'loan_id': loan.id})
                    if loan.d_or_m_or_y == 'd':
                        date_start = date_start + relativedelta(days=loan.pay)
                    if loan.d_or_m_or_y == 'm':
                        date_start = date_start + relativedelta(months=loan.pay)
                    if loan.d_or_m_or_y == 'y':
                        date_start = date_start + relativedelta(years=loan.pay)
                else:
                    if amount>0:
                        self.env['loan.line'].create({
                            'amount': amount,
                            'number': i,
                            'date': date_start,
                            'loan_id': loan.id})
                        if loan.d_or_m_or_y == 'd':
                            date_start = date_start + relativedelta(days=loan.pay)
                        if loan.d_or_m_or_y == 'm':
                            date_start = date_start + relativedelta(months=loan.pay)
                        if loan.d_or_m_or_y == 'y':
                            date_start = date_start + relativedelta(years=loan.pay)

        self.state = 'do'
        return True

        # for loan in self:
        #
        #         amount = loan.first_amount
        #         vals = []
        #         date_start = loan.date
        #
        #
        #         amount=loan.loan_amount
        #         vals=[]
        #         date_start = loan.date
        #     for i in range(1,loan.num_of_loan + 1):
        #         print(i)
        #
        #         for record in loan.loans_ids:
        #             loan.write({'loans_ids': [(2, record.id)]})
        #
        #         vals.append((0, 0, {
        #             'amount':amount,
        #             'number':i,
        #             'date':date_start,
        #             'loan_id':loan.id
        #
        #             }))
        #         if loan.d_or_m_or_y == 'd':
        #             date_start = date_start + relativedelta(days=loan.pay)
        #         if loan.d_or_m_or_y == 'm':
        #             date_start = date_start + relativedelta(months=loan.pay)
        #         if loan.d_or_m_or_y == 'y':
        #             date_start = date_start + relativedelta(years=loan.pay)
        #         print(vals)
        #
        #         loan.update({'loans_ids': vals})
        # self.state='do'
        #
        # return True


class loan(models.Model):
    _name = 'loan.line'
    name = fields.Text(required=False, )
    number = fields.Char("Number")
    amount = fields.Float("Amount")
    date = fields.Date(string="Date", required=False, )
    is_paid =fields.Boolean(string="Is Paid",  )
    loan_id = fields.Many2one(
        'loan'
    )
    payment_id = fields.Many2one(comodel_name='account.payment', string="Payment", required=False,)
