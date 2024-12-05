{
    'name': 'Nova Invoice Report Model USA',
    'version': '1.0',
    'summary': 'Custom invoice report model for USA',
    'description': 'This module provides a custom invoice report model for USA.',
    'author': 'Chema Fernández <Nova Cartografia>',
    'category': 'Accounting',
    'depends': ['account'],
    'data': [
        # Add your data files here
        'views/nova_invoice_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}