# -*- coding: utf-8 -*-
##############################################################################

import datetime
from odoo import api, fields, models, _

class print_so_shipping(models.AbstractModel):
    _name = 'report.print_so_shipping.temp_so_shipping'

    @api.model
    def get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'data': data,
            'docs': docids,
        }
