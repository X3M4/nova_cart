{
    'name': 'CRM Lead Rejected Stage',
    'version': '1.0',
    'summary': 'Module to add a rejected stage to CRM leads',
    'description': 'This module adds a rejected stage to CRM leads in Odoo.',
    'author': 'Your Name',
    'website': 'http://www.yourcompany.com',
    'category': 'Sales',
    'depends': ['crm', 'mail'],
    'data': [
        # Add your data files here
        'security/ir.model.access.csv',
        'views/crm_lead_custom_views.xml',
        'views/crm_rejected_reason_views.xml',
        'views/crm_lead_custom_buttons.xml',
        'views/crm_lead_search_view_custom.xml',
        'wizard/crm_lead_rejected_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}