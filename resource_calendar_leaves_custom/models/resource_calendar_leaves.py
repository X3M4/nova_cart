from odoo import models, fields, api, _
from datetime import datetime

class ResourceCalendarCustom(models.Model):
    _inherit = 'resource.calendar'

    @api.model
    def _get_default_global_leaves(self):
        current_year = datetime.now().year
        return [
            (0, 0, {'name': 'Año Nuevo', 'date_from': f'{current_year}-01-01 00:00:00', 'date_to': f'{current_year}-01-02 00:00:00'}),
            (0, 0, {'name': 'Reyes', 'date_from': f'{current_year}-01-06 00:00:00', 'date_to': f'{current_year}-01-07 00:00:00'}),
            (0, 0, {'name': 'Día de la Constitución', 'date_from': f'{current_year}-12-06 00:00:00', 'date_to': f'{current_year}-12-07 00:00:00'}),
            (0, 0, {'name': 'Viernes Santo', 'date_from': f'{current_year}-04-18 00:00:00', 'date_to': f'{current_year}-04-19 00:00:00'}),
            (0, 0, {'name': 'Día del Trabajador', 'date_from': f'{current_year}-05-01 00:00:00', 'date_to': f'{current_year}-05-02 00:00:00'}),
            (0, 0, {'name': 'Asunción de la Virgen', 'date_from': f'{current_year}-08-15 00:00:00', 'date_to': f'{current_year}-08-16 00:00:00'}),
            (0, 0, {'name': 'Fiesta Nacional de España', 'date_from': f'{current_year}-10-12 00:00:00', 'date_to': f'{current_year}-10-13 00:00:00'}),
            (0, 0, {'name': 'Todos los Santos', 'date_from': f'{current_year}-11-01 00:00:00', 'date_to': f'{current_year}-11-02 00:00:00'}),
            (0, 0, {'name': 'Inmaculada Concepción', 'date_from': f'{current_year}-12-08 00:00:00', 'date_to': f'{current_year}-12-09 00:00:00'}),
            (0, 0, {'name': 'Navidad', 'date_from': f'{current_year}-12-25 00:00:00', 'date_to': f'{current_year}-12-26 00:00:00'}),
        ]

    @api.model
    def update_global_leaves(self):
        current_year = datetime.now().year
        leaves = self.env['resource.calendar.leaves'].search([('resource_id', '=', False)])
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

    global_leave_ids = fields.One2many(
        'resource.calendar.leaves', 'calendar_id', 'Global Leaves',
        domain=[('resource_id', '=', False)], default=_get_default_global_leaves
    )