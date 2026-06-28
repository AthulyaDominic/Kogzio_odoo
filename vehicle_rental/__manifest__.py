{
    'name':'Vehicle Rental',
    'version':"19.0.1.1",
    'summary':'Vehicle rental management module',
    'description': 'Custom module for managing rental vehicles.',
    'author': 'Athulya Dominic',
    'category': 'Services',
    'depends': ['base',    'account', 'product','mail','website',
],
    'data': [
'security/security.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
         'data/product_data.xml',
        'data/vehicleid_sequence.xml',
        'data/rental_request_sequence.xml',
         'views/search_views.xml',
        'views/vehicle_rental_views.xml',

        'views/vehicle_feature_views.xml',
        'views/rental_request_views.xml',
        'views/website.xml',
        'wizard/rental_report_wizard_view.xml',

        'views/vehicle_menu.xml',
        'views/website_menu.xml',


        'report/rental_request_report.xml'

    ],
'assets': {
        'web.assets_frontend': [
            'vehicle_rental/static/src/js/rental_period.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}