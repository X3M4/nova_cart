from odoo import models, api, fields, _

class LaptopController(models.Model):
    _name = 'laptop.controller'
    _description = 'Laptop Controler'

    name = fields.Char(string='Name', required=True, computed = '_compute_name', store=True)
    
    model = fields.Many2one('product.template', string='Model', required=True, domain=[('name', 'ilike', 'portátil p')])
    
    status = fields.Selection([
        ('available', 'Available'),
        ('not_available', 'Not Available'),
    ], string='Status', required=True, default='available', computed = '_compute_status', store=True)
    
    laptop_movements_line_ids = fields.One2many(
        string='Laptop Movements Line',
        comodel_name='laptop.movements.line',
        inverse_name='laptop_controller_id',
    )
    
    laptop_movement_line_count = fields.Integer(
        string='Laptop Movement Line Count',
        compute='laptop_movement_line_ids_count',
    )
    
                
    @api.onchange('model')
    def _onchange_model(self):
        if self.model:
            self.name = self.model.name

    def _update_status(self):
        for record in self:
            # Obtener el último movimiento registrado
            last_movement = record.laptop_movements_line_ids.sorted(key=lambda r: r.delivery_date, reverse=True)[:1]
            new_status = 'not_available' if last_movement and not last_movement.return_date else 'available'
            
            # Solo actualizar si el estado realmente ha cambiado
            if record.status != new_status:
                record.status = new_status

    @api.model
    def create(self, vals):
        # Llamar al método padre para crear el registro
        record = super(LaptopController, self).create(vals)
        # Actualizar el estado inmediatamente después de crear el registro
        record._update_status()
        return record

    def write(self, vals):
        # Llamar al método padre para guardar los cambios
        result = super(LaptopController, self).write(vals)
        # Solo actualizar el estado si es necesario
        self._update_status()
        return result



class LaptopMovementsLine(models.Model):
    _name = 'laptop.movements.line'
    _description = 'Laptop Movements Line'

    laptop_controller_id = fields.Many2one(
        'laptop.controller', 
        string='Laptop Controller', 
        ondelete='cascade',
        default=lambda self: self.env.context.get('laptop_controller_id', False),
    )
    worker = fields.Many2one('hr.employee', string='Worker',)
    delivery_date = fields.Date(string='Delivery date')
    return_date = fields.Date(string='Return date', store=True, )
    
    @api.model
    def create(self, vals):
        # Comprobar si no se está proporcionando un valor para laptop_controller_id
        if 'laptop_controller_id' not in vals:
            # Asignar automáticamente el laptop_controller_id si se ha proporcionado laptop_controller_id en laptop_movements_line_ids
            laptop_controller = self.env['laptop.controller'].search([('laptop_movements_line_ids', '=', vals.get('id'))], limit=1)
            if laptop_controller:
                vals['laptop_controller_id'] = laptop_controller.id
        # Crear el registro
        return super(LaptopMovementsLine, self).create(vals)