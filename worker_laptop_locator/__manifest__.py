{
    'name': 'Worker Laptop Locator',
    'version': '1.0',
    'summary': 'Module to locate worker laptops',
    'description': 'This module helps in locating worker laptops within the organization.',
    'author': 'Chema Fernández <Nova Cartografia>',
    'website': 'http://www.yourcompany.com',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/groups.xml',
        'security/ir.model.access.csv',
        'views/worker_laptop_locator_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}