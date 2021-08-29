
{
    'name': 'Ninos Shipping Company',
    'summary': 'Ninos Shipping Company',
    'author': "ITSS , Mahmoud Elfeky",
    'company': 'ITSS',
    'website': "http://www.itss-c.com",
    'version': '14.0.0.1.0',
    'category': 'Inventory',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'sale',
        'stock',
        'delivery',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'report/',
        # 'wizard/',
        'views/shipping_company.xml',
        'views/delivery_carrier.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

