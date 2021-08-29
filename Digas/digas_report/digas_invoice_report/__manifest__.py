{
    'name': 'Digas Invoices Report',
    'summary': 'Digas Invoices Report',
    'author': "ITSS , Ezz Eldin Saleh",
    'company': 'ITSS',
    'website': "http://www.itss-c.com",
    'version': '14.0.0.1.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'account',
        'degas_account_customize',
        'jt_amount_in_words',
    ],
    'data': [
        # 'wizard/',
        'report/report_invoices.xml',
        # 'views/res_company.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

