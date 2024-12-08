# -*- coding: utf-8 -*-

from odoo import api, fields, models

class CrmLeadRejected(models.TransientModel):
    _name = 'crm.lead.rejected'
    _description = 'Get Rejected Reason'

    rejected_reason_id = fields.Many2one('crm.rejected.reason', 'Rejected Reason')

    @api.multi
    def action_rejected_reason_apply(self):
        leads = self.env['crm.lead'].browse(self.env.context.get('active_ids'))
        leads.write({'rejected_reason_id': self.rejected_reason_id.id})
        leads.action_set_rejected()
        return {'type': 'ir.actions.act_window_close'}