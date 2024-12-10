from odoo import models, fields, api
from odoo.exceptions import UserError
import pdb

class CrmLeadCustom(models.Model):
    _inherit = 'crm.lead'
    
    is_rejected = fields.Boolean(string='Is Rejected', default=False, track_visibility='always')
    is_lost = fields.Boolean(string='Is Lost', default=False)
    is_won = fields.Boolean(string='Is Won', default=False)
    rejected_reason_id = fields.Many2one('crm.rejected.reason', string='Rejected Reason', track_visibility='always')

    
    @api.multi
    def action_set_rejected(self):
        # pdb.set_trace()
        self.action_check_all_registers()
        self.is_rejected = True
        self.is_lost = False
        self.is_won = False

        self.write({'probability': 0.05, 
                    'active': True, 
                    'lost_reason': False, 
                    'is_rejected': True, 
                    'is_lost': False,
                    'is_won': False})
        # return {
        #     'name': 'Rejected Reason',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'crm.lead.rejected',
        #     'view_mode': 'form',
        #     'view_id': self.env.ref('crm_lead_rejected_stage.crm_lead_rejected_view_form').id,
        #     'target': 'new',
        #     'context': {
        #         'default_lead_id': self.id,  # Pasar el ID del lead al wizard
        #     },
        # }
    
    @api.multi
    def action_set_lost(self):
        """ Lost semantic: probability = 0, active = False """
        self.action_check_all_registers()
        self.is_lost = True
        self.is_rejected = False
        self.is_won = False
        self.rejected_reason_id = False
        return self.write({'probability': 0,
                           'active': False, 
                           'rejected_reason_id': False,
                           'is_lost': True,
                           'is_rejected': False,
                           'is_won': False})
    
    @api.multi
    def action_set_won(self):
        """ Won semantic: probability = 100 (active untouched) """
        self.action_check_all_registers()
        for lead in self:
            self.is_lost = False
            self.is_rejected = False
            self.is_won = True
            # stage_id = lead._stage_find(domain=[('probability', '=', 100.0), ('on_change', '=', True)])
            # lead.write({'stage_id': stage_id.id, 'probability': 100})
            return self.write({'probability': 100, 
                               'active': True, 
                               'rejected_reason_id': False,
                               'lost_reason': False,
                               'is_won': True,
                               'is_lost': False,
                               'is_rejected': False})
    
    @api.multi
    def action_check_all_registers(self):
        leads = self.env['crm.lead'].search([])
        for l in leads:
            if l.probability == 0 and l.active == False:
                l.write({
                    'is_lost': True,
                    'is_rejected': False,
                    'is_won': False,
                    'rejected_reason_id': False},)
            elif l.probability == 100:
                l.write({
                    'is_won':True,
                    'is_lost': False,
                    'is_rejected': False,
                    'rejected_reason_id': False,
                    'lost_reason' : False},)
            else:
                l.write({
                    'is_rejected': True,
                    'is_lost': False,
                    'is_won': False,
                    'lost_reason': False})
    
class RejectedReason(models.Model):
    _name = 'crm.rejected.reason'
    _description = 'Rejected Reason'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Reason', required=True,track_visibility='always')
    active = fields.Boolean('Active', default=True)