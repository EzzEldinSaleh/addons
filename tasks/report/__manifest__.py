# -*- coding: utf-8 -*-
{
    'name': "report sale",
    'summary': """
    """,
    'description': """
    """,
    'author': "CDS Solutions SRL",
    'website': "www.cdsegypt.com",
    'contributors': [
        'Ramadan Khalil <rkhalil1990@gmail.com>',
    ],
    'version': '0.1',
    'depends': ['base','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/view.xml',
        'views/report_xlsx.xml',
        'views/wizard_reporting.xml'
    ],
}
