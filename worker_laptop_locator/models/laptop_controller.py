from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class LaptopController(models.Model):
    _name = 'laptop.controller'
    _description = 'Laptop Controler'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Name', required=True, computed='_compute_name', store=True, track_visibility='always')
    
    model = fields.Many2one('product.template', string='Model', required=True, domain=[('name', 'ilike', 'port')], track_visibility='always')
    
    status = fields.Selection([
        ('available', 'Available'),
        ('not_available', 'Not Available'),
    ], string='Status', required=True, default='available', computed='_compute_status', store=True, track_visibility='always')
    
    laptop_movements_line_ids = fields.One2many(
        string='Laptop Movements Line',
        comodel_name='laptop.movements.line',
        inverse_name='laptop_controller_id',
        track_visibility='always'
    )
    
    # laptop_movement_line_count = fields.Integer(
    #     string='Laptop Movement Line Count',
    #     compute='laptop_movement_line_ids_count',
    #     track_visibility='always'
    # )
    
    owner = fields.Char(string='Owner', compute='_compute_owner', store=True, track_visibility='always')

    @api.depends('laptop_movements_line_ids.return_date', 'laptop_movements_line_ids.delivery_date')
    def _compute_owner(self):
        for record in self:
            last_movement = record.laptop_movements_line_ids.sorted(key=lambda r: r.delivery_date, reverse=True)[:1]
            if last_movement:
                last_movement = last_movement[0]
                record.owner = last_movement.worker.name if not last_movement.return_date else ''
            else:
                record.owner = ''
                
    @api.onchange('model')
    def _onchange_model(self):
        if self.model:
            self.name = self.model.name.upper()

    def _update_status(self):
        for record in self:
            last_movement = record.laptop_movements_line_ids.sorted(key=lambda r: r.delivery_date, reverse=True)[:1]
            new_status = 'not_available' if last_movement and not last_movement.return_date else 'available'
            
            if record.status != new_status:
                record.status = new_status

    @api.model
    def create(self, vals):
        record = super(LaptopController, self).create(vals)
        record._update_status()
        return record

    def write(self, vals):
        result = super(LaptopController, self).write(vals)
        self._update_status()
        return result


class LaptopMovementsLine(models.Model):
    _name = 'laptop.movements.line'
    _description = 'Laptop Movements Line'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    laptop_controller_id = fields.Many2one(
        'laptop.controller', 
        string='Laptop Controller', 
        ondelete='cascade',
        default=lambda self: self.env.context.get('laptop_controller_id', False),
        track_visibility='always'
    )
    worker = fields.Many2one('hr.employee', string='Worker', track_visibility='always')
    delivery_date = fields.Date(string='Delivery date', required=True, store=True, default=fields.Date.today, track_visibility='always')
    return_date = fields.Date(string='Return date', store=True, track_visibility='always')
    
    @api.model
    def create(self, vals):
        if 'laptop_controller_id' not in vals:
            laptop_controller = self.env['laptop.controller'].search([('laptop_movements_line_ids', '=', vals.get('id'))], limit=1)
            if laptop_controller:
                vals['laptop_controller_id'] = laptop_controller.id
        return super(LaptopMovementsLine, self).create(vals)
    
    @api.constrains('delivery_date', 'return_date')
    def _check_return_date(self):
        for record in self:
            if record.delivery_date and record.return_date and record.delivery_date > record.return_date:
                raise ValidationError(_('Return date must be greater than delivery date.'))
