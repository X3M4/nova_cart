from odoo import models, fields, api
from odoo.exceptions import UserError
import pdb

class CrmLeadCustom(models.Model):
    _inherit = 'crm.lead'
    
    is_rejected = fields.Boolean(string='Is Rejected', default=True)
    is_lost = fields.Boolean(string='Is Lost', default=True)
    is_won = fields.Boolean(string='Is Won', default=True)

    
    @api.multi
    def action_set_rejected(self):
        # pdb.set_trace()
        self.is_won = False
        self.is_lost = False
        self.is_rejected = True
        pdb.set_trace()
        # return self.write({'probability': 0.1})
        return self.write({'probability': 50})
    
    @api.multi
    def action_set_lost(self):
        """ Lost semantic: probability = 0, active = False """
        self.is_won = False
        self.is_lost = True
        self.is_rejected = False
        self.write({'probability': 0, 'active': False})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Rechazo Realizado',
                'message': 'La probabilidad se ha actualizado a 0 y el registro se ha desactivado.',
                'type': 'info',  # 'info', 'warning', 'danger'
                'sticky': False,
            },
        }
    
    @api.multi
    def action_set_won(self):
        """ Won semantic: probability = 100 (active untouched) """
        for lead in self:
            self.is_won = True
            self.is_lost = False
            self.is_rejected = False
            stage_id = lead._stage_find(domain=[('probability', '=', 100.0), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 100})