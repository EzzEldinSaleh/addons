# -*- coding: utf-8 -*-

{
    'name': "Cupio Snacks POS Customizations",
    'summary': """
        Cupio Snacks POS Customizations""",
    'description': """
        Cupio Snacks POS Customizations
    """,
    'author': "ITSS , Mahmoud Naguib",
    'website': "http://www.itss-c.com",
    'category': 'Point Of Sale',
    'license': "LGPL-3",
    'version': '14.0.1.0',
    'depends': ['point_of_sale'],
    'data': [
        'views/assets.xml',
        'views/res_partner.xml',
        'views/uom_uom.xml',
    ],
    'qweb': [
        'static/src/xml/OrderWidget.xml',
        'static/src/xml/OrderSummary.xml',
        'static/src/xml/PaymentMethodButton.xml',
    ],
}
