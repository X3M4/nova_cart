from odoo import models, fields, api, _
from datetime import datetime
import sys
from datetime import timedelta

class UpdateGlobalLeaveIds(models.TransientModel):
    _name = 'update.global.leave.ids'
    _description = 'Update Global Leave Ids'
    
    year = fields.Integer('Year', required=True, default=lambda self: fields.datetime.now().year)
    
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

    def wizard_update_global_leave_ids(self):
        self.ensure_one()
        current_year = self.year
        leaves = self.env['resource.calendar.leaves'].search([('resource_id', '=', False)])
        calendars = self.env['resource.calendar'].search([('global_leave_ids', '!=', False)])
        
        # import pdb; pdb.set_trace()
    
        for leave in leaves:
            if leave.name == 'Año Nuevo':
                leave.write({
                    'date_from': datetime(self.year, 1, 1, 0, 0, 0),
                    'date_to': datetime(self.year, 1, 1, 23, 59, 59)
                })
            elif leave.name == 'Reyes':
                leave.write({
                    'date_from': datetime(self.year, 1, 6, 0, 0, 0),
                    'date_to': datetime(self.year, 1, 6, 23, 59, 59)
                })
            elif leave.name == 'Día de la Constitución':
                leave.write({
                    'date_from': datetime(self.year, 12, 6, 0, 0, 0),
                    'date_to': datetime(self.year, 12, 6, 23, 59, 59)
                })
            elif leave.name == 'Jueves Santo':
                thursday, friday = self.calculate_holy_thursday_good_friday(self.year)
                leave.write({
                    'date_from': thursday,
                    'date_to': thursday + timedelta(days=1) - timedelta(hours=1)
                })
            elif leave.name == 'Viernes Santo':
                thursday, friday = self.calculate_holy_thursday_good_friday(self.year)
                leave.write({
                    'date_from': friday,
                    'date_to': friday + timedelta(days=1) - timedelta(hours=1)
                })
            elif leave.name == 'Día del Trabajador':
                leave.write({
                    'date_from': datetime(self.year, 5, 1, 0, 0, 0),
                    'date_to': datetime(self.year, 5, 1, 23, 59, 59)
                })
            elif leave.name == 'Asunción de la Virgen':
                leave.write({
                    'date_from': datetime(self.year, 8, 15, 0, 0, 0),
                    'date_to': datetime(self.year, 8, 15, 23, 59, 59)
                })
            elif leave.name == 'Fiesta Nacional de España':
                leave.write({
                    'date_from': datetime(self.year, 10, 12, 0, 0, 0),
                    'date_to': datetime(self.year, 10, 12, 23, 59, 59)
                })
            elif leave.name == 'Todos los Santos':
                leave.write({
                    'date_from': datetime(self.year, 11, 1, 0, 0, 0),
                    'date_to': datetime(self.year, 11, 1, 23, 59, 59)
                })
            elif leave.name == 'Inmaculada Concepción':
                leave.write({
                    'date_from': datetime(self.year, 12, 8, 0, 0, 0),
                    'date_to': datetime(self.year, 12, 8, 23, 59, 59)
                })
            elif leave.name == 'Navidad':
                leave.write({
                    'date_from': datetime(self.year, 12, 25, 0, 0, 0),
                    'date_to': datetime(self.year, 12, 25, 23, 59, 59)
                })
            print(f"Actualizado: {leave.name}, {leave.date_from} - {leave.date_to}".encode(sys.stdout.encoding, errors='replace').decode())
