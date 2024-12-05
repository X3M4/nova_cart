from odoo import models, fields, api

class RejectedReason(models.Model):
    _name = 'crm.rejected.reason'
    _description = 'Rejected Reason'

    name = fields.Char('Reason', required=True)
    active = fields.Boolean('Active', default=True)