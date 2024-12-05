from odoo import models, fields, api, _

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    leer_info_privada = fields.Boolean(
        string='Leer Información Privada',
        default=False,
        help='Indica si el usuario puede ver información privada.'
    )