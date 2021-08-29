from odoo import api, fields, models
class reportsaleanalysis(models.AbstractModel):
    _name = 'report.report_sale_analysis.sale_analysis_report'

    @api.model
    def _get_report_values(self, docids, data=None):

            # get the report action back as we will need its data
        report = self.env['ir.actions.report']._get_report_from_name('report_sale_analysis.sale_analysis_report')
        docs = self.env['sale.order'].browse(docids[0])
        product=[]
        customer=[]
        customers=data['form']['customer_ids']
        products=data['form']['product_ids']
        # for i in customers:
        #     customer.append(
        #         {
        #             'name':i.name
        #         }
        #     )

        saleorders = self.env['sale.order'].search([])
        for x in saleorders:
            customer.append(
                    {
                        'name':x.name,
                    }
                )

            # for k in saleorders:
            #     for x in k.order_line:
            #         if x.id.origin or x.id.ref:
            #             for s in product:
            #                 if not x.product_id.id == s.product_id.id:
            #                     product.append(x)





        return {
                    'doc_model': 'sale.wizard.report',
                    'cus': customer,
            'docs': docs,

                }









