# -*- coding: utf-8 -*-
{
    'name':  "Account Invoice Reports",

    'summary': """ Create Group of Account Invoice Reports""",

    'author': "ITSS , Omnia Sameh",
    'website': "http://www.itss-c.com",

    'category': 'Invoicing',
    'version': '12.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': [
                'account',
                'account_beneficiary_bank',
                'sale_bill_of_lading',
                'base_company_data',
                'base_partner_fields',
                'sale_letter_of_credit',
                'base_terms_conditions',
                ],

    # always loaded
    'data': [
            'views/account_invoice.xml',
            'views/report_commercial_account_invoice.xml',
            'views/report_commercial_account_invoice_with_tax.xml',
            'views/report_detailed_packing_list.xml',
            'views/report_beneficiary_certification.xml',
            'views/report_beneficiary_shipment_advice.xml',
            'views/report_beneficiary_bill_of_exchange.xml',
    ],
}
