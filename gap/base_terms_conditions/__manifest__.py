# -*- coding: utf-8 -*-
{
    'name': "Base Terms And Conditions",
    'summary': """Create Multiple Records For Terms And Conditions """,
    'author':  "ITSS, Omnia Sameh, Omnia Sameh",
    'website': "http://www.itss-c.com",
    'category': 'base',
    'version': '12.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
         'security/ir.model.access.csv',
         'views/base_terms_and_conditions.xml',
    ],
    # only loaded in demonstration mode
}
