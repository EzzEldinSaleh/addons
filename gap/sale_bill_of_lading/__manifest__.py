# -*- coding: utf-8 -*-
{
    'name':  "Sales Bill Of Lading ",

    'summary': """ Create Sale Order's Bill Of Lading With Detailed Report """,

    'author': "ITSS , Omnia Sameh",
    'website': "http://www.itss-c.com",

    'category': 'sales',
    'version': '12.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'sales_team', 'sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/bill_of_lading_sequence.xml',
        'views/sale_bill_of_lading.xml',
        'views/sale_order.xml',
        'views/report_sale_bill_of_lading.xml',
    ],
}
