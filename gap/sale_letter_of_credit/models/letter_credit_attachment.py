# -*- coding: utf-8 -*-
""" init object """
from odoo import fields, models, api, _ ,tools, SUPERUSER_ID
from odoo.exceptions import ValidationError,UserError
from datetime import datetime , date ,timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from dateutil.relativedelta import relativedelta
from odoo.fields import Datetime as fieldsDatetime
import calendar
from odoo import http
from odoo.http import request
from odoo import tools

import logging

LOGGER = logging.getLogger(__name__)


class LetterCreditAttachment(models.Model):
    _name = 'sale.letter.credit.attachment'
    _rec_name = 'name'
    _description = 'Letter Of Credit Documents'

    name = fields.Char()
    document = fields.Binary(required=True  )
    letter_credit_id = fields.Many2one(comodel_name="sale.letter.credit", string="", required=False, )
