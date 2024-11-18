{
    'name': 'Product Template Custom Fields',
    'version': '1.0',
    'summary': 'Add custom fields to product templates',
    'description': 'This module allows you to add custom fields to product templates in Odoo.',
    'author': 'Chema Fernández <Nova Cartografia>',
    'website': 'http://www.yourwebsite.com',
    'category': 'Product',
    'depends': ['product'],
    'data': [
        'views/product_template_custom_fields_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}