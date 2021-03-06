# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vendor_type = fields.Selection(default="consignment", selection=[('consignment', 'Consignment'), ('cash', 'Cash'), ], required=False, )
