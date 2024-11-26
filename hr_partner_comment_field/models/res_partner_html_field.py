from odoo import models, fields, api, _

class ResPartnerHtmlField(models.Model):
    _inherit = 'res.partner'
    
    comment = fields.Html(
        string = "Candidate Comment",
        help = "Comment about the Human Resources candidate",
        readonly = False,
    )
    
    @api.model
    def create(self, vals):
        record = super(ResPartnerHtmlField, self).create(vals)
        return record
    

    
    
    