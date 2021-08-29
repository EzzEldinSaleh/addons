# -*- coding: utf-8 -*-
""" Sale Bill Of Lading"""

from odoo import api, fields, models


class BillOfLading(models.Model):
    _name = 'sale.bill.of.lading'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'bl_seq'

    order_id = fields.Many2one(
        comodel_name='sale.order',
        required=True,
        track_visibility='always'
    )

    shipper_id = fields.Many2one(
        comodel_name="res.partner",
        track_visibility='always'
    )

    consignee_id = fields.Many2one(
        comodel_name="res.partner",
    )
    first_notify_party_id = fields.Many2one(
        comodel_name="res.partner",
    )
    second_notify_party_id = fields.Many2one(
        comodel_name="res.partner",
    )
    port_of_lading = fields.Char(
        track_visibility='always'
    )
    port_of_discharge = fields.Char(
        track_visibility='always'
    )

    vessel = fields.Char(string="Vessel(s)", track_visibility='always')
    voyage_no = fields.Char("Voyage No.", track_visibility='always')

    place_of_delivery = fields.Char(track_visibility='always')
    place_of_receipt = fields.Char(track_visibility='always')

    no_original_bl = fields.Char("No. of Original BL", track_visibility='always')
    carrier_name = fields.Char(track_visibility='always')
    bgk_number = fields.Char(string="BGK Number", track_visibility='always')
    place = fields.Char(track_visibility='always')
    date = fields.Date(track_visibility='always')
    movement_list = fields.Selection(
        selection=[('fcl', 'FCL'), ('lcl', 'LCL'), ],
        track_visibility='always')

    remarks = fields.Text()
    bl_seq = fields.Char(
        copy=False,
        readonly=True,
        index=True,
        track_visibility='always'
    )
    freight_and_charges = fields.Text(string="Freight & Charges",
                                      track_visibility='always')
    container_nos = fields.Char(track_visibility='always')
    seal_nos = fields.Char(string="Seal Nos.",
                           track_visibility='always')
    nu_container = fields.Char(string='No. of Containers',
                               track_visibility='always')
    nu_package = fields.Char(string='No. of Packages',
                             track_visibility='always')
    measures = fields.Char(track_visibility='always')
    gross_weight = fields.Char(track_visibility='always')
    total_gross_weight = fields.Char(track_visibility='always')
    total_net_weight = fields.Char(track_visibility='always')
    description = fields.Text(string="Item/Description",
                              track_visibility='always')
    freight = fields.Selection(
        selection=[('Freight Collect', 'Freight Collect'), ('Freight Prepaid', 'Freight Prepaid'), ],
        track_visibility='always')
    shipment = fields.Selection(
        selection=[('Shipped On board', 'Shipped On board'), ('Received For Shipment', 'Received For Shipment'), ],
        track_visibility='always')
    state = fields.Selection(
        string="Status",
        default="draft",
        selection=[('draft', 'Draft'), ('original', 'Original Bill Of Lading'), ],
        track_visibility='always'
    )
    bl_line_ids = fields.One2many(
        string="Shipment Lines",
        comodel_name='sale.bill.of.lading.line',
        inverse_name="bl_id",
    )

    @api.multi
    def write(self, vals):
        if 'date' in vals and self.state == 'draft':
            vals['state'] = 'original'
        return super(BillOfLading, self).write(vals)

    @api.model
    def create(self, vals):
        vals['bl_seq'] = self.env['ir.sequence'].next_by_code('bill.of.lading.seq')
        if 'date' in vals:
            vals['state'] = 'original'
        result = super(BillOfLading, self).create(vals)
        return result


class BillOfLadingLine(models.Model):

    _name = 'sale.bill.of.lading.line'
    _description = "Bill Of Lading lines"

    seal_nos = fields.Char(string="Seal Nos.")
    nu_container = fields.Char(string='No. of Containers')
    bags_no = fields.Integer()
    gw = fields.Integer(string="GW", )
    nw = fields.Integer(string="NW",)
    container_size = fields.Selection(selection=[('ft', '40ft / 40'), ('hq', 'HQ / 20ft'), ], )
    bl_id = fields.Many2one(comodel_name="sale.bill.of.lading", ondelete='cascade')
