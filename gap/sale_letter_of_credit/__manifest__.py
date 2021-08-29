# -*- coding: utf-8 -*-
{
    'name': "Letter Of Credit",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ITSS, Mahmoud Naguib",
    'website': "http://www.itss-c.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account','sale',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/letter_credit.xml',
        'views/letter_credit_type.xml',
        'views/sale_order.xml',
        'views/account_invoice.xml',
    ],

}
