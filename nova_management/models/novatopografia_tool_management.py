from odoo import models, fields, api, _
from odoo.exceptions import UserError

class NovatopographyToolManagement(models.Model):
    _name = 'novatopografia.tool.management'
    _description = 'Novatopografia Tool Management'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'employee'
    
    employee = fields.Many2one('hr.employee', string='Employee', required=True, track_visibility='always')
    
    tool_movements_line_ids = fields.One2many(
        string='Novatopografia Tool Movements Line',
        comodel_name='tool.movement.line',
        inverse_name='data_management_id',
        track_visibility='always'
    )
    
class ToolMovementLine(models.Model):
    _name = 'tool.movement.line'
    _description = 'Tool Movement Line'
    _rec_name = 'delivery_date'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    
    data_management_id = fields.Many2one(
        'novatopografia.tool.management',
        string='Data Management',
        required=True,
        track_visibility='always'
    )
    
    delivery_date = fields.Datetime(
        string='Delivery Date', 
        required=True,
        default=fields.Datetime.now, 
        track_visibility='always'
    )
    
    return_date = fields.Datetime(
        string='Return Date', 
        track_visibility='always',
        compute='_compute_return_date'
    )
    
    @api.depends('state')
    def _compute_return_date(self):
        for record in self:
            if record.state == 'returned':
                record.return_date = fields.Datetime.now()
            else:
                record.return_date = False
    
    employee_supplier = fields.Many2one(
        'hr.employee', 
        string='Employee Supplier', 
        required=True, 
        track_visibility='always',
    )
    
    state = fields.Selection([
        ('delivered', 'Delivered'),
        ('returned', 'Returned')],
        string='State', 
        default='delivered', 
        track_visibility='always'
    )
    
    stock_move_line_ids = fields.One2many(
        string='Stock Move Line',
        comodel_name='stock.tool.move.line',
        inverse_name='movement_line_id',
        track_visibility='always'
    )
    
    notes = fields.Html(
        string='Notes',
        track_visibility='always'
    )
    
    @api.multi
    def action_edit_stock_move_lines(self):
        # Cambiar el estado o realizar alguna acción con las líneas
        # Si deseas abrir un formulario para editar las líneas de stock_move_line_ids:
        return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Stock Move Lines',
            'res_model': 'stock.move.line',
            'view_mode': 'form',
            'domain': [('id', 'in', self.stock_move_line_ids.ids)],  # Filtra las líneas asociadas a este registro
            'target': 'current',
        }

class StockToolMoveLine(models.Model):
    _name = 'stock.tool.move.line'
    _description = 'Novatopografia Tool Movements Line'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    
    movement_line_id = fields.Many2one(
        'tool.movement.line',
        string='Tool Movement Line',
        required=True,
        track_visibility='always'
    )

    picking_type_id = fields.Many2one(
        'stock.picking.type', 
        string='Operation type', 
        required=True,
        track_visibility='always'
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        track_visibility='always',
        default=lambda self: self.env.ref('base.res_partner_0', raise_if_not_found=False)
    )
    
    project_id = fields.Many2one(
        'project.project', 
        string='Project', 
        track_visibility='always'
    )
    
    scheduled_date = fields.Datetime(
        string='Fecha Programada', 
        default=fields.Datetime.now, 
        track_visibility='always'
    )
    
    origin = fields.Char(
        string='Origen', 
        track_visibility='always'
    )
    
    location_id = fields.Many2one(
        'stock.location', 
        string='Ubicación de Origen', 
        required=True, 
        track_visibility='always'
    )
    
    location_dest_id = fields.Many2one(
        'stock.location', 
        string='Ubicación de Destino', 
        required=True, 
        track_visibility='always'
    )
    
    product_id = fields.Many2one(
        'product.product', 
        string='Producto', 
        required=True, 
        track_visibility='always'
    )
    
    qty_saved = fields.Integer(
        string='Cantidad Guardada',
        track_visibility='always',
        related='product_id.qty_available',
    )
        
    
    quantity = fields.Float(
        string='Cantidad', 
        required=True, 
        default=1.0, 
        track_visibility='always'
    )
    
    
    def create_stock_picking_and_move(self):
        """Crea una operación de picking y un movimiento de stock"""
        self.ensure_one()

        # Crear picking
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.picking_type_id.id,
            'partner_id': self.partner_id.id,
            'scheduled_date': self.scheduled_date,
            'origin': self.origin,
        })

        # Crear movimiento de stock
        move = self.env['stock.move'].create({
            'picking_id': picking.id,
            'partner_id': self.partner_id.id,
            'name': f"Movimiento de {self.product_id.name}",
            'product_id': self.product_id.id,
            'product_uom_qty': self.quantity,
            'product_uom': self.product_id.uom_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
        })

        # Confirmar picking y movimiento
        picking.action_confirm()
        picking.action_assign()
        picking.button_validate()

        return {'type': 'ir.actions.act_window_close'}