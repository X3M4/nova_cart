from odoo import models, fields, api, _
from datetime import datetime
import sys
from datetime import timedelta
import pytz

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
        thursday, friday = self.calculate_holy_thursday_good_friday(self.year)
        monday_easter = self.calculate_easter_date(self.year) +  timedelta(days=1)
        
        user_tz = self.env.user.tz or 'UTC'
        local = pytz.timezone(user_tz)
        
        def to_naive_utc(date):
            """Convierte una fecha a UTC y la hace naive."""
            localized_date = local.localize(date)
            utc_date = localized_date.astimezone(pytz.UTC)
            return utc_date.replace(tzinfo=None)
        
        for leave in leaves:
            if leave.name == 'Jueves Santo':
                leave.write({
                    'date_from': to_naive_utc(thursday),
                    'date_to': to_naive_utc(thursday.replace(hour=23, minute=59, second=59))
                })
            elif leave.name == 'Viernes Santo':
                leave.write({
                    'date_from': to_naive_utc(friday),
                    'date_to': to_naive_utc(friday.replace(hour=23, minute=59, second=59))
                })
            elif leave.name == 'Lunes de Pascua':
                leave.write({
                    'date_from': to_naive_utc(monday_easter),
                    'date_to': to_naive_utc(monday_easter.replace(hour=23, minute=59, second=59))
                })
            elif leave.name == 'San Vicente Ferrer':
                san_vicente = monday_easter + timedelta(days=7)
                leave.write({
                    'date_from': to_naive_utc(san_vicente),
                    'date_to': to_naive_utc(san_vicente.replace(hour=23, minute=59, second=59))
                })
            elif leave.name == 'Corpus Christi':
                corpus_christi = monday_easter + timedelta(days=60)
                leave.write({
                    'date_from': to_naive_utc(corpus_christi),
                    'date_to': to_naive_utc(corpus_christi.replace(hour=23, minute=59, second=59))
                })
            else:
                # Calcular fechas desde cero basándose en el año actual
                original_date_from = leave.date_from.replace(year=current_year) + timedelta(days=1)
                original_date_to = leave.date_to.replace(year=current_year)

                new_date_from = datetime(
                    current_year, 
                    original_date_from.month, 
                    original_date_from.day, 
                    0, 0, 0
                )
                new_date_to = datetime(
                    current_year, 
                    original_date_to.month, 
                    original_date_to.day, 
                    23, 59, 59
                )

                # Validar que `date_from` sea anterior a `date_to`
                if new_date_from > new_date_to:
                    new_date_to = new_date_from + timedelta(days=1)

                leave.write({
                    'date_from': to_naive_utc(new_date_from),
                    'date_to': to_naive_utc(new_date_to)
                })
            print(f"Actualizado: {leave.name}, {leave.date_from} - {leave.date_to}".encode(sys.stdout.encoding, errors='replace').decode())