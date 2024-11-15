{
    'name': 'Project Task Line',
    'version': '1.0',
    'summary': 'Module to manage project task lines',
    'description': 'This module allows you to manage project task lines in Odoo.',
    'author': 'Your Name',
    'website': 'http://www.yourwebsite.com',
    'category': 'Project',
    'depends': [
        'project',
        'product',
        'sale',
        ],
    'data': [
        'secutiry/ir.model.access.csv',
        'views/project_task_line_views.xml',
        'views/product_template_custom.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}