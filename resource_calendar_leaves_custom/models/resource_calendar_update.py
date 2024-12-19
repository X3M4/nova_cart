from odoo import models, fields, api

class ResourceCalendarUpdate(models.Model):
    _name = 'resource.calendar.update'
    _description = 'Resource Calendar Update'

    # def action_update_global_leave_ids(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Update Global Leave Ids',
    #         'res_model': 'update.global.leave.ids',
    #         'view_mode': 'form',
    #         'target': 'new',
    #     }
    
    def action_update_global_leave_ids(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Global Leave Ids',
            'res_model': 'update.global.leave.ids',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_calendar_id': self.id,
            }
        }