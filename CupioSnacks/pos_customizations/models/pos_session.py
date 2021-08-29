# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = 'pos.session'

    def action_pos_session_validate(self):
        if self.config_id.cash_control and (not self.cash_register_id or not self.cash_register_id.cashbox_end_id):
            raise ValidationError(_('Please Set Closing Balance!'))
        return super(PosSession, self).action_pos_session_validate()

    @api.constrains('user_id', 'state')
    def _check_unicity(self):
        # open if there is no session in 'opening_control', 'opened', 'closing_control' for one user
        if self.search_count([
                ('state', 'not in', ('closed', 'closing_control')),
                ('user_id', '=', self.user_id.id),
                ('rescue', '=', False)
            ]) > 1:
            raise ValidationError(_("You cannot create two active sessions with the same responsible."))
