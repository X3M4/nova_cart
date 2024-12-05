{
    'name': 'CRM Lead Rejected Stage',
    'version': '1.0',
    'summary': 'Module to add a rejected stage to CRM leads',
    'description': 'This module adds a rejected stage to CRM leads in Odoo.',
    'author': 'Your Name',
    'website': 'http://www.yourcompany.com',
    'category': 'Sales',
    'depends': ['crm'],
    'data': [
        # Add your data files here
        'views/set_lost_custom_button.xml',
        'views/crm_lead_custom_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}