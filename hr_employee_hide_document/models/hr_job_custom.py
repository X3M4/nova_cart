from odoo import models, api, fields, _

class HrJobCustom(models.Model):
    _inherit = 'hr.job'

    hide_document = fields.Boolean(string='Hide Document', default=False, compute='_compute_hide_document', store=True)
    
    @api.onchange('hide_document')
    
