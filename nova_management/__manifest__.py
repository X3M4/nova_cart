{
    'name': 'nova_management',
    'version': '1.0',
    'summary': 'Module to manage Nova Cartographia operations',
    'description': 'This module installs management tools.',
    'author': 'Chema Fernández <Nova Cartografia>',
    'website': 'http://www.yourcompany.com',
    'category': 'Tools',
    'depends': ['base', 'mail', 'portal',],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/worker_laptop_locator_views.xml',
        'views/novatopografia_tool_management_views.xml',
        'views/tool_movement_line_views.xml',
        'views/novacartografia_management_menu.xml',
    ],
    'images': ['static/description/icon.png',
               'static/description/icon.svg'],
    'installable': True,
    'application': True,
    'auto_install': False,
}