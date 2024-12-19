{
    'name': 'Resource Calendar Leaves Custom',
    'version': '1.0',
    'summary': 'Customizations for resource calendar leaves',
    'description': 'This module provides customizations for resource calendar leaves.',
    'author': 'Chema Fernandez<Nova Cartografia>',
    'category': 'Human Resources',
    'depends': ['base', 'resource'],
    'data': [
        # Add your data files here
        'data/resource_calendar_leaves_custom.xml',
        'views/resource_calendar_leaves_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}