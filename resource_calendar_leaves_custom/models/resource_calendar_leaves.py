from odoo import models, fields, api, _
from datetime import datetime, timedelta
import pytz

class ResourceCalendarCustom(models.Model):
    _inherit = 'resource.calendar'
    
    state = fields.Selection(string='State', 
                             selection=[('andalucia', 'Andalucía'), 
                                        ('aragon', 'Aragón'), 
                                        ('asturias', 'Asturias'), 
                                        ('baleares', 'Baleares'), 
                                        ('canarias', 'Canarias'), 
                                        ('cantabria', 'Cantabria'), 
                                        ('castilla_la_mancha', 'Castilla-La Mancha'), 
                                        ('castilla_y_leon', 'Castilla y León'), 
                                        ('cataluna', 'Cataluña'), 
                                        ('ceuta', 'Ceuta'), 
                                        ('extremadura', 'Extremadura'), 
                                        ('galicia', 'Galicia'), 
                                        ('madrid', 'Madrid'), 
                                        ('melilla', 'Melilla'), 
                                        ('murcia', 'Murcia'), 
                                        ('navarra', 'Navarra'), 
                                        ('pais_vasco', 'País Vasco'), 
                                        ('la_rioja', 'La Rioja'), 
                                        ('valencia', 'Valencia'), ], 
                             default='andalucia')
    
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
        thursday, friday = self.calculate_holy_thursday_good_friday(current_year)
        
        user_tz = self.env.user.tz or 'UTC'
        local = pytz.timezone(user_tz)
        
        def to_naive_utc(date):
            """Convierte una fecha a UTC y la hace naive."""
            localized_date = local.localize(date)
            utc_date = localized_date.astimezone(pytz.UTC)
            return utc_date.replace(tzinfo=None)
        
        global_holidays = [
            (0, 0, {'name': 'Año Nuevo', 'date_from': to_naive_utc(datetime(current_year, 1, 1, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 1, 1, 23, 59, 59))}),
            (0, 0, {'name': 'Reyes', 'date_from': to_naive_utc(datetime(current_year, 1, 6, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 1, 6, 23, 59, 59))}),
            (0, 0, {'name': 'Jueves Santo', 'date_from': to_naive_utc(thursday), 'date_to': to_naive_utc(thursday.replace(hour=23, minute=59, second=59))}),
            (0, 0, {'name': 'Viernes Santo', 'date_from': to_naive_utc(friday), 'date_to': to_naive_utc(friday.replace(hour=23, minute=59, second=59))}),
            (0, 0, {'name': 'Día del Trabajador', 'date_from': to_naive_utc(datetime(current_year, 5, 1, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 5, 1, 23, 59, 59))}),
            (0, 0, {'name': 'Asunción de la Virgen', 'date_from': to_naive_utc(datetime(current_year, 8, 15, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 8, 15, 23, 59, 59))}),
            (0, 0, {'name': 'Fiesta Nacional de España', 'date_from': to_naive_utc(datetime(current_year, 10, 12, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 10, 12, 23, 59, 59))}),
            (0, 0, {'name': 'Todos los Santos', 'date_from': to_naive_utc(datetime(current_year, 11, 1, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 11, 1, 23, 59, 59))}),
            (0, 0, {'name': 'Día de la Constitución', 'date_from': to_naive_utc(datetime(current_year, 12, 6, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 12, 6, 23, 59, 59))}),
            (0, 0, {'name': 'Inmaculada Concepción', 'date_from': to_naive_utc(datetime(current_year, 12, 8, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 12, 8, 23, 59, 59))}),
            (0, 0, {'name': 'Navidad', 'date_from': to_naive_utc(datetime(current_year, 12, 25, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 12, 25, 23, 59, 59))}),
        ]
        
        if self.state == 'andalucia':
            global_holidays.append((0, 0, {'name': 'Día de Andalucía', 'date_from': to_naive_utc(datetime(current_year, 2, 28, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 2, 28, 23, 59, 59))}))
        elif self.state == 'aragon':
            global_holidays.append((0, 0, {'name': 'Día de Aragón', 'date_from': to_naive_utc(datetime(current_year, 4, 23, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 4, 23, 23, 59, 59))}))
        elif self.state == 'asturias':
            global_holidays.append((0, 0, {'name': 'Día de Asturias', 'date_from': to_naive_utc(datetime(current_year, 9, 8, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 9, 8, 23, 59, 59))}))
        elif self.state == 'baleares':
            global_holidays.append((0, 0, {'name': 'Día de las Islas Baleares', 'date_from': to_naive_utc(datetime(current_year, 3, 1, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 3, 1, 23, 59, 59))}))
            global_holidays.append((0, 0, {'name': 'San Esteban', 'date_from': to_naive_utc(datetime(current_year, 12, 26, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 12, 26, 23, 59, 59))}))
        elif self.state == 'canarias':
            global_holidays.append((0, 0, {'name': 'Día de Canarias', 'date_from': to_naive_utc(datetime(current_year, 5, 30, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 5, 30, 23, 59, 59))}))
        elif self.state == 'cantabria':
            global_holidays.append((0, 0, {'name': 'Día de Cantabria', 'date_from': to_naive_utc(datetime(current_year, 7, 28, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 7, 28, 23, 59, 59))}))
            global_holidays.append((0, 0, {'name': 'La Bien Aparecida', 'date_from': to_naive_utc(datetime(current_year, 9, 15, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 9, 15, 23, 59, 59))}))
        elif self.state == 'castilla_la_mancha':
            global_holidays.append((0, 0, {'name': 'Día de Castilla-La Mancha', 'date_from': to_naive_utc(datetime(current_year, 5, 31, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 5, 31, 23, 59, 59))}))
            corpus = self.calculate_easter_date(current_year) + timedelta(days=60)
            global_holidays.append((0, 0, {'name': 'Corpus Christi', 'date_from': to_naive_utc(corpus), 'date_to': to_naive_utc(corpus.replace(hour=23, minute=59, second=59))}))
        elif self.state == 'castilla_y_leon':
            global_holidays.append((0, 0, {'name': 'Día de Castilla y León', 'date_from': to_naive_utc(datetime(current_year, 4, 23, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 4, 23, 23, 59, 59))}))
        elif self.state == 'cataluna':
            global_holidays.remove((0, 0, {'name': 'Jueves Santo', 'date_from': to_naive_utc(thursday), 'date_to': to_naive_utc(thursday.replace(hour=23, minute=59, second=59))}))
            monday_easter = self.calculate_easter_date(current_year) + timedelta(days=1)
            global_holidays.append((0, 0, {'name': 'Lunes de Pascua', 'date_from': to_naive_utc(monday_easter), 'date_to': to_naive_utc(monday_easter.replace(hour=23, minute=59, second=59))}))
            global_holidays.append((0, 0, {'name': 'San Juan', 'date_from': to_naive_utc(datetime(current_year, 6, 24, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 6, 24, 23, 59, 59))}))
            global_holidays.append((0, 0, {'name': 'Día de Cataluña', 'date_from': to_naive_utc(datetime(current_year, 9, 11, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 9, 11, 23, 59, 59))}))
            global_holidays.append((0, 0, {'name': 'San Esteban', 'date_from': to_naive_utc(datetime(current_year, 12, 26, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 12, 26, 23, 59, 59))}))
        elif self.state == 'valencia':
            global_holidays.remove((0, 0, {'name': 'Jueves Santo', 'date_from': to_naive_utc(thursday), 'date_to': to_naive_utc(thursday.replace(hour=23, minute=59, second=59))}))
            global_holidays.append((0, 0, {'name': 'San José', 'date_from': to_naive_utc(datetime(current_year, 3, 19, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 3, 19, 23, 59, 59))}))
            monday_easter = self.calculate_easter_date(current_year) + timedelta(days=1)
            global_holidays.append((0, 0, {'name': 'Lunes de Pascua', 'date_from': to_naive_utc(monday_easter), 'date_to': to_naive_utc(monday_easter.replace(hour=23, minute=59, second=59))}))
            global_holidays.append((0, 0, {'name': 'San Vicente Ferrer', 'date_from': to_naive_utc(monday_easter + timedelta(days=7)), 'date_to': to_naive_utc((monday_easter + timedelta(days=7)).replace(hour=23, minute=59, second=59))}))
            global_holidays.append((0, 0, {'name': 'Día de la Comunidad Valenciana', 'date_from': to_naive_utc(datetime(current_year, 10, 9, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 10, 9, 23, 59, 59))}))
        elif self.state == 'extremadura':
            global_holidays.append((0, 0, {'name': 'Día de Extremadura', 'date_from': to_naive_utc(datetime(current_year, 9, 8, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 9, 8, 23, 59, 59))}))
        elif self.state == 'galicia':
            global_holidays.append((0, 0, {'name': 'Día de Galicia', 'date_from': to_naive_utc(datetime(current_year, 7, 25, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 7, 25, 23, 59, 59))}))
            global_holidays.append((0, 0, {'name': 'Día de las Letras Gallegas', 'date_from': to_naive_utc(datetime(current_year, 5, 17, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 5, 17, 23, 59, 59))}))
            global_holidays.append((0, 0, {'name': 'Santiago Apóstol', 'date_from': to_naive_utc(datetime(current_year, 7, 25, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 7, 25, 23, 59, 59))}))
        elif self.state == 'madrid':
            global_holidays.append((0, 0, {'name': 'Día de la Comunidad de Madrid', 'date_from': to_naive_utc(datetime(current_year, 5, 2, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 5, 2, 23, 59, 59))}))
        elif self.state == 'la_rioja':
            global_holidays.append((0, 0, {'name': 'Día de La Rioja', 'date_from': to_naive_utc(datetime(current_year, 6, 9, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 6, 9, 23, 59, 59))}))
        elif self.state == 'pais_vasco':
            monday_easter = self.calculate_easter_date(current_year) + timedelta(days=1)
            global_holidays.append((0, 0, {'name': 'Lunes de Pascua', 'date_from': to_naive_utc(monday_easter), 'date_to': to_naive_utc(monday_easter.replace(hour=23, minute=59, second=59))}))
            global_holidays.append((0, 0, {'name': 'Santiago Apóstol', 'date_from': to_naive_utc(datetime(current_year, 7, 25, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 7, 25, 23, 59, 59))}))
        elif self.state == 'murcia':
            global_holidays.append((0, 0, {'name': 'Día de la Región de Murcia', 'date_from': to_naive_utc(datetime(current_year, 6, 9, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 6, 9, 23, 59, 59))}))
        elif self.state == 'ceuta':
            global_holidays.append((0, 0, {'name': 'Día de Ceuta', 'date_from': to_naive_utc(datetime(current_year, 9, 2, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 9, 2, 23, 59, 59))}))
        elif self.state == 'melilla':
            global_holidays.append((0, 0, {'name': 'Día de Melilla', 'date_from': to_naive_utc(datetime(current_year, 9, 17, 0, 0, 0)), 'date_to': to_naive_utc(datetime(current_year, 9, 17, 23, 59, 59))}))

        global_holidays = sorted(global_holidays, key=lambda x: x[2]['date_from'])
        
        return global_holidays

    global_leave_ids = fields.One2many(
        'resource.calendar.leaves', 'calendar_id', 'Global Leaves',
        domain=[('resource_id', '=', False)], default=_get_default_global_leaves
    )
    
    @api.onchange('state')
    def _onchange_state(self):
        if self.state:
            # for leave in self.global_leave_ids:
            #     leave.unlink()
            self.global_leave_ids = [(5, 0, 0)]
            self.global_leave_ids = self._get_default_global_leaves()