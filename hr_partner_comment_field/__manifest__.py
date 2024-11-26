{
    'name': 'HR Partner Comment Field',
    'version': '1.0',
    'summary': 'Adds a comment field to HR partner records',
    'description': 'This module adds a comment field to HR partner records in Odoo.',
    'author': 'Your Name',
    'website': 'http://www.yourwebsite.com',
    'category': 'Human Resources',
    'depends': ['base', 'hr'],
    'data': [
        # List your data files here, e.g. 'views/hr_partner_comment_field_view.xml'
        'views/res_partner_html_field.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}