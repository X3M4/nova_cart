from odoo import models, fields, api, _
from datetime import datetime

class ResourceCalendarCustom(models.Model):
    _inherit = 'resource.calendar'
    
    def calculate_easter_date(self, year):
        """Calculate the date of Easter Sunday using the Gauss algorithm."""
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month = (h + l - 7 * m + 114) // 31  # March = 3, April = 4
        day = ((h + l - 7 * m + 114) % 31) + 1
        return datetime(year, month, day, 0, 0, 0)

    def calculate_holy_thursday_good_friday(self, year):
        """Calculate the dates of Holy Thursday and Good Friday for a given year."""
        from datetime import date, timedelta

        # Calculate Easter Sunday
        
        easter_sunday = self.calculate_easter_date(year)

        # Holy Thursday is 3 days before Easter Sunday
        holy_thursday = easter_sunday - timedelta(days=3)
        # Good Friday is 2 days before Easter Sunday
        good_friday = easter_sunday - timedelta(days=2)

        return holy_thursday, good_friday

    @api.model
    def _get_default_global_leaves(self):
        current_year = datetime.now().year
        thursday,friday = self.calculate_holy_thursday_good_friday(current_year)
        return [
            (0, 0, {'name': 'Año Nuevo', 'date_from': fields.Datetime.from_string(f'{current_year}-01-01'), 'date_to': fields.Datetime.from_string(f'{current_year}-01-02')}),
            (0, 0, {'name': 'Reyes', 'date_from': fields.Datetime.from_string(f'{current_year}-01-06 00:00:00'), 'date_to': fields.Datetime.from_string(f'{current_year}-01-07 00:00:00')}),
            (0, 0, {'name': 'Día de la Constitución', 'date_from': fields.Datetime.from_string(f'{current_year}-12-06 00:00:00'), 'date_to': fields.Datetime.from_string(f'{current_year}-12-07 00:00:00')}),
            (0, 0, {'name': 'Jueves Santo', 'date_from': thursday, 'date_to': thursday}),
            (0, 0, {'name': 'Viernes Santo', 'date_from': friday, 'date_to': friday}),
            (0, 0, {'name': 'Día del Trabajador', 'date_from': fields.Datetime.from_string(f'{current_year}-05-01 00:00:00'), 'date_to': fields.Datetime.from_string(f'{current_year}-05-02 00:00:00')}),
            (0, 0, {'name': 'Asunción de la Virgen', 'date_from': fields.Datetime.from_string(f'{current_year}-08-15 00:00:00'), 'date_to': fields.Datetime.from_string(f'{current_year}-08-16 00:00:00')}),
            (0, 0, {'name': 'Fiesta Nacional de España', 'date_from': fields.Datetime.from_string(f'{current_year}-10-12 00:00:00'), 'date_to': fields.Datetime.from_string(f'{current_year}-10-13 00:00:00')}),
            (0, 0, {'name': 'Todos los Santos', 'date_from': fields.Datetime.from_string(f'{current_year}-11-01 00:00:00'), 'date_to': fields.Datetime.from_string(f'{current_year}-11-02 00:00:00')}),
            (0, 0, {'name': 'Inmaculada Concepción', 'date_from': fields.Datetime.from_string(f'{current_year}-12-08 00:00:00'), 'date_to': fields.Datetime.from_string(f'{current_year}-12-09 00:00:00')}),
            (0, 0, {'name': 'Navidad', 'date_from': fields.Datetime.from_string(f'{current_year}-12-25 00:00:00'), 'date_to': fields.Datetime.from_string(f'{current_year}-12-26 00:00:00')}),
        ]

    # @api.model
    # def update_global_leaves(self):
    #     current_year = datetime.now().year
    #     leaves = self.env['resource.calendar.leaves'].search([('resource_id', '=', False)])
    #     for leave in leaves:
    #         if leave.name == 'Año Nuevo':
    #             leave.date_from = fields.Datetime.from_string(f'{current_year}-01-01 00:00:00')
    #             leave.date_to = datetime(current_year, 1, 2, 0, 0, 0)
    #         elif leave.name == 'Reyes':
    #             leave.date_from = datetime(current_year, 1, 6, 0, 0, 0)
    #             leave.date_to = datetime(current_year, 1, 7, 0, 0, 0)
    #         elif leave.name == 'Día de la Constitución':
    #             leave.date_from = datetime(current_year, 12, 6, 0, 0, 0)
    #             leave.date_to = datetime(current_year, 12, 7, 0, 0, 0)
    #         elif leave.name == 'Viernes Santo':
    #             leave.date_from = datetime(current_year, 4, 18, 0, 0, 0)
    #             leave.date_to = datetime(current_year, 4, 19, 0, 0, 0)
    #         elif leave.name == 'Día del Trabajador':
    #             leave.date_from = datetime(current_year, 5, 1, 0, 0, 0)
    #             leave.date_to = datetime(current_year, 5, 2, 0, 0, 0)
    #         elif leave.name == 'Asunción de la Virgen':
    #             leave.date_from = datetime(current_year, 8, 15, 0, 0, 0)
    #             leave.date_to = datetime(current_year, 8, 16, 0, 0, 0)
    #         elif leave.name == 'Fiesta Nacional de España':
    #             leave.date_from = datetime(current_year, 10, 12, 0, 0, 0)
    #             leave.date_to = datetime(current_year, 10, 13, 0, 0, 0)
    #         elif leave.name == 'Todos los Santos':
    #             leave.date_from = datetime(current_year, 11, 1, 0, 0, 0)
    #             leave.date_to = datetime(current_year, 11, 2, 0, 0, 0)
    #         elif leave.name == 'Inmaculada Concepción':
    #             leave.date_from = datetime(current_year, 12, 8, 0, 0, 0)
    #             leave.date_to = datetime(current_year, 12, 9, 0, 0, 0)
    #         elif leave.name == 'Navidad':
    #             leave.date_from = datetime(current_year, 12, 25, 0, 0, 0)
    #             leave.date_to = datetime(current_year, 12, 26, 0, 0, 0)

    global_leave_ids = fields.One2many(
        'resource.calendar.leaves', 'calendar_id', 'Global Leaves',
        domain=[('resource_id', '=', False)], default=_get_default_global_leaves
    )