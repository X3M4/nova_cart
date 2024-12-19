from odoo import models, fields, api, _
from datetime import datetime

class UpdateGlobalLeaveIds(models.TransientModel):
    _name = 'update.global.leave.ids'
    _description = 'Update Global Leave Ids'
    
    year = fields.Integer('Year', required=True, default=lambda self: fields.datetime.now().year + 1)
    preview = fields.Html('Preview', compute='_compute_preview')
    
    def _compute_preview(self):
        self.ensure_one()
        leaves = self.env['resource.calendar.leaves'].search([('resource_id', '=', False)])
        preview = '<ul>'
        for leave in leaves:
            preview += f'<li>{leave.name}: {leave.date_from} - {leave.date_to}</li><br>'
        preview += '</ul>'
        self.preview = preview

    def update_global_leave_ids(self):
        self.ensure_one()
        current_year = self.year
        leaves = self.env['resource.calendar.leaves'].search([('resource_id', '=', False)])
        calendars = self.env['resource.calendar'].search(['global_leave_ids', '!=', False])
    
        for leave in leaves:
            if leave.name == 'Año Nuevo':
                leave.date_from = f'{current_year}-01-01 00:00:00'
                leave.date_to = f'{current_year}-01-02 00:00:00'
            elif leave.name == 'Reyes':
                leave.date_from = f'{current_year}-01-06 00:00:00'
                leave.date_to = f'{current_year}-01-07 00:00:00'
            elif leave.name == 'Día de la Constitución':
                leave.date_from = f'{current_year}-12-06 00:00:00'
                leave.date_to = f'{current_year}-12-07 00:00:00'
            elif leave.name == 'Viernes Santo':
                leave.date_from = f'{current_year}-04-18 00:00:00'
                leave.date_to = f'{current_year}-04-19 00:00:00'
            elif leave.name == 'Día del Trabajador':
                leave.date_from = f'{current_year}-05-01 00:00:00'
                leave.date_to = f'{current_year}-05-02 00:00:00'
            elif leave.name == 'Asunción de la Virgen':
                leave.date_from = f'{current_year}-08-15 00:00:00'
                leave.date_to = f'{current_year}-08-16 00:00:00'
            elif leave.name == 'Fiesta Nacional de España':
                leave.date_from = f'{current_year}-10-12 00:00:00'
                leave.date_to = f'{current_year}-10-13 00:00:00'
            elif leave.name == 'Todos los Santos':
                leave.date_from = f'{current_year}-11-01 00:00:00'
                leave.date_to = f'{current_year}-11-02 00:00:00'
            elif leave.name == 'Inmaculada Concepción':
                leave.date_from = f'{current_year}-12-08 00:00:00'
                leave.date_to = f'{current_year}-12-09 00:00:00'
            elif leave.name == 'Navidad':
                leave.date_from = f'{current_year}-12-25 00:00:00'
                leave.date_to = f'{current_year}-12-26 00:00:00'