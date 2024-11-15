from odoo import models, fields, api, _


class ProjectTaskLine(models.Model):
    _name = 'project.task.line'
    _description = 'Project Task Line'

    name = fields.Char(string='Description', required=True)
    description = fields.Text(string='Client Description')
    objective = fields.Float(string='Objective')
    unit = fields.Many2one('uom.uom', string='Unit of Measure')
    time = fields.Float(string='Time (Hours)')
    time_x_hour = fields.Float(string='Objj/Time (Hours)')
    workers = fields.Integer(string='Workers')
    receptor = fields.Char(string='Receptors')
    price = fields.Float(string='Price')
    
    
    sale_order_line_id = fields.Many2one(
        string='Sale Order Line',
        comodel_name='sale.order.line',
        ondelete='restrict',
    )
    

    