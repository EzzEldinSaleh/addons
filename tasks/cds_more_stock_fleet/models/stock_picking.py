# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#    Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date


class StockPicking(models.Model):
    _inherit = "stock.picking"

    vehicle_id = fields.Many2one('fleet.vehicle', 'Car')
    driver_id = fields.Many2one('res.partner', 'Driver')

    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        if self.vehicle_id and self.vehicle_id.driver_id:
            self.driver_id = self.vehicle_id.driver_id
