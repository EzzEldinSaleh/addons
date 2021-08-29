# -*- coding: utf-8 -*-
{
    'name': "Retail Sales Report",

    'summary': """
        Retail Sales Report """,


    'author': "ITSS , Mahmoud Naguib",
    'website': "http://www.itss-c.com",

    'category': 'Point Of Sale',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale',
                'product_tags',
                'actual_sale_price',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/retail_sales_report_wizard.xml',
        'views/res_partner.xml',
        'report/report_retail_sales.xml',
    ],



}