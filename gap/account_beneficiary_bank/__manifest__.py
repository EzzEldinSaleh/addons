# -*- coding: utf-8 -*-
{
    'name':  "Account Invoice Commercial Bank",

    'summary': """ Create Commercial Customer Invoice Bank""",
    'author': "ITSS , Omnia Sameh",
    'website': "http://www.itss-c.com",
    'category': 'Invoicing',
    'version': '12.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['account',],
    # always loaded
    'data': [
        'views/account_journal.xml',
    ],
}
