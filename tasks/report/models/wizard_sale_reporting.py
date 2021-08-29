from odoo import api, fields, models
class wizardsale(models.TransientModel):
    _name = 'sale.wizard'

    date_from = fields.Date(string="Date From", required=True, )
    date_to = fields.Date(string="Date To", required=True, )
    product_ids = fields.Many2many(comodel_name="product.template", string="Products", )
    customer_ids = fields.Many2many(comodel_name="res.partner", string="Customers",required=True, )
    def print_sale_analysis(self):
        data = {
            'model': 'sale.wizard',
            'form': self.read()[0]
        }

        return self.env.ref('report.report_sale_id_ez').with_context(landscape=True).report_action(self,
                                                                                                         data=data)
