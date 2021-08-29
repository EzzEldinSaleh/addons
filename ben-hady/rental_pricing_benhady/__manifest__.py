
{
    'name': 'Rental Pricing Ben hady',
    'summary': 'Rental Pricing Ben hady',
    'author': "ITSS , Mahmoud Elfeky",
    'company': 'ITSS',
    'website': "http://www.itss-c.com",
    'version': '14.0.0.1.0',
    'category': 'Rental',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'sale_renting',
        'stock',
        'product',
        'uom',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'report/',
        # 'wizard/',
        'views/rental_pricing.xml',
        'views/product_template.xml',
        'data/product_data.xml',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

