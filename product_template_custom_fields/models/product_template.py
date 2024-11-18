from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    objective = fields.Float(string='Objective', help='Objective of the product')
    unit = fields.Many2one('product.uom', string='Unit', help='Unit of the product')
    time = fields.Integer(string='Time', help='Time of the product in hours')
    target = fields.Float(string='Target', help='Target of the product')
    number_of_workers = fields.Integer(string='Number of workers', help='Number of workers needed for the product')
    receptors = fields.Char(string='Receptors', help='Receptors of the product')