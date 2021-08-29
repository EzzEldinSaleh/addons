# -*- encoding: utf-8 -*-

{
    'name': 'POS Gift Receipt',
    'description': """
        POS Gift Receipt
""",
    'version': '14.0.1',
    'license': '',
    'summary': """POS Gift Receipt""",
    'category': 'Point of Sale',
    'author': "Mahmoud Naguib, ITSS <https://www.itss-c.com>",
    'website': "https://www.itss-c.com",
    'depends': ['point_of_sale'],
    'demo': [],
    'data': [
        'views/point_of_sale.xml',
     ],
    'qweb': [
        'static/xml/PrintGiftReceiptButton.xml',
        # 'static/xml/OrderReceipt.xml',
        'static/xml/ReprintReceiptScreen.xml',
    ],
    'installable': True,
}
