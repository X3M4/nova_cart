from odoo import models, fields, api, _

class ProductTemplateWithTasks(models.Model):
    
    _inherit = ['product.template']
    
    
    project_task_line_ids = fields.One2many(
        string='Project Task Line',
        comodel_name='project.task.line',
        inverse_name='sale_order_line_id',
    )