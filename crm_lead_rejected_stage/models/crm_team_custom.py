from odoo import models, fields, api
from odoo.tools.safe_eval import safe_eval

class CrmTeam(models.Model):
    _inherit = 'crm.team'
    
    member_ids = fields.Many2many(
        'res.users', 
        'crm_team_res_users_rel', 
        'crm_team_id', 
        'user_id', 
        string='Members')

    @api.model
    def action_your_pipeline(self):
        # Obtener la acción predeterminada
        action = self.env.ref('crm.crm_lead_opportunities_tree_view').read()[0]
        user_team_id = self.env.user.sale_team_id.id
        
        if user_team_id:
            # Garantizar que el equipo es accesible en multi-compañía
            user_team_id = self.search([('id', '=', user_team_id)], limit=1).id
        else:
            user_team_id = self.search([], limit=1).id
            action['help'] = _("""<p class='o_view_nocontent_smiling_face'>Add new opportunities</p><p>
            Looks like you are not a member of a Sales Team. You should add yourself
            as a member of one of the Sales Team.
            </p>""")
            if user_team_id:
                action['help'] += _("<p>As you don't belong to any Sales Team, Odoo opens the first one by default.</p>")

        # Configurar el contexto
        action_context = safe_eval(action['context'], {'uid': self.env.uid})
        if user_team_id:
            action_context['default_team_id'] = user_team_id

        # **Aplicar el dominio modificado** para filtrar asignados al usuario actual
        # action['domain'] = [('user_id', '=', self.env.uid)]
        
        # Pasar el contexto modificado
        action['context'] = action_context
        return action