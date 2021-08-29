# -*- coding: utf-8 -*-
#########################################################################

{
    'name': 'Degas Accounting Customize',
    'version': '14.0.1.0.0',
    'summary': """""",
    'category': "Accounting",
    'description': """
       * This addon help you for :
       1 -  connect invoice with picking
       2 -  connect customer followup report with picking
    """,
    'author': 'Ahmed Amen',
    'depends': ['sale','account','stock','account_reports'],
    'data': [
             # 'security/ir.model.access.csv',
             'views/view.xml',
             'views/invoice_report.xml',
             'views/sale_order.xml',

             ],
    'demo': [
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
}
