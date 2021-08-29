""" Initialize Po Type """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class Project(models.Model):
    """
        Initialize Po Type:
         -
    """
    _name = 'project'
    _description = 'Project'

    name = fields.Char(
        required=True,
        translate=True,
    )
    project_line_ids = fields.One2many(
        'project.line',
        'project_id'
    )


class ProjectLine(models.Model):
    """
        Initialize Project Line:
         -
    """
    _name = 'project.line'
    _description = 'Project Line'
    _rec_name = 'project_id'

    start_date = fields.Date()
    end_date = fields.Date()
    project_id = fields.Many2one(
        'project'
    )
    partner_id = fields.Many2one(
        'res.partner'
    )
