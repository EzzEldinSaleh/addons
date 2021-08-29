
{
    'name': 'Change Partner For Draft Invoices !',
    'summary': 'Change Partner For Draft Invoices !',
    'author': "ITSS , Mahmoud Elfeky",
    'company': 'ITSS',
    'website': "http://www.itss-c.com",
    'version': '14.0.0.1.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'report/',
        'wizard/change_partner.xml',
        # 'views/',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

