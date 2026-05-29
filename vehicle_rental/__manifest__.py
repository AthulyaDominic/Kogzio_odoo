{
    'name':'Vehicle Rental',
    'version':"19.0.1.1",
    'summary':'Vehicle rental management module',
    'description': 'Custom module for managing rental vehicles.',
    'author': 'Athulya Dominic',
    'category': 'Services',
    'depends': ['base',    'account',
],
    'data': [
        'security/ir.model.access.csv',
        'data/vehicleid_sequence.xml',
        'data/rental_request_sequence.xml',
         'views/search_views.xml',
        'views/vehicle_rental_views.xml',

        'views/vehicle_feature_views.xml',
        'views/rental_request_views.xml',

        'views/vehicle_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}