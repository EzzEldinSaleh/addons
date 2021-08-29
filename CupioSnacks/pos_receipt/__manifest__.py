{
    'name': 'Pos Receipt Customization',
    'summary': 'Pos Receipt Customization',
    'author': "ITSS , Mahmoud Elfeky",
    'company': 'ITSS',
    'website': "http://www.itss-c.com",
    'version': '14.0.0.1.0',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'point_of_sale',
        'pos_customizations',
        # 'pos_sales_person',
        'pos_gift_receipt',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'report/',
        # 'wizard/',
        'views/assets.xml',
        # 'data/',
    ],
    'qweb': [
        'static/src/xml/pos_receipt_view.xml'
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

