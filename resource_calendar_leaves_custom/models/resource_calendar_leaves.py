from odoo import models, fields, api, _

class ResourceCalendarCustom(models.Model):
    _inherit = 'resource.calendar'

    @api.model
    def _get_default_global_leaves(self):
        return [
            (0, 0, {'name': 'Año Nuevo', 'date_from': '2025-01-01 00:00:00', 'date_to': '2025-01-02 00:00:00'}),
            (0, 0, {'name': 'Reyes', 'date_from': '2025-01-06 00:00:00', 'date_to': '2025-01-07 00:00:00'}),
            (0, 0, {'name': 'Día de la Constitución', 'date_from': '2025-12-06 00:00:00', 'date_to': '2025-12-07 00:00:00'}),
            (0, 0, {'name': 'Viernes Santo', 'date_from': '2025-04-18 00:00:00', 'date_to': '2025-04-19 00:00:00'}),
            (0, 0, {'name': 'Día del Trabajador', 'date_from': '2025-05-01 00:00:00', 'date_to': '2025-05-02 00:00:00'}),
            (0, 0, {'name': 'Asunción de la Virgen', 'date_from': '2025-08-15 00:00:00', 'date_to': '2025-08-16 00:00:00'}),
            (0, 0, {'name': 'Fiesta Nacional de España', 'date_from': '2025-10-12 00:00:00', 'date_to': '2025-10-13 00:00:00'}),
            (0, 0, {'name': 'Todos los Santos', 'date_from': '2025-11-01 00:00:00', 'date_to': '2025-11-02 00:00:00'}),
            (0, 0, {'name': 'Inmaculada Concepción', 'date_from': '2025-12-08 00:00:00', 'date_to': '2025-12-09 00:00:00'}),
            (0, 0, {'name': 'Navidad', 'date_from': '2025-12-25 00:00:00', 'date_to': '2025-12-26 00:00:00'}),
        ]

    global_leave_ids = fields.One2many(
        'resource.calendar.leaves', 'calendar_id', 'Global Leaves',
        domain=[('resource_id', '=', False)], default=_get_default_global_leaves
    )