# -*- coding: utf-8 -*-
{
    'name':  "Base Company Data",

    'summary': """ Add New Fields To Company & Partners """,

    'author': "ITSS , Omnia Sameh",
    'website': "http://www.itss-c.com",

    'category': 'base',
    'version': '12.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/res_company.xml',
    ],
}
