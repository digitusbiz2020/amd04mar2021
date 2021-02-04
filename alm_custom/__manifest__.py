{
    'name': 'ALM',
    'version': '14.0.0',
    "category": "Sales,stock,Accounting",
    'summary': 'ALM',
    "author": "Planet-odoo",
    'website': 'http://www.planet-odoo.com/',
    'depends': ['base','sale','mrp','project','purchase_stock'],
    'data': [
            'security/ir.model.access.csv',
            'views/sale_order_view.xml',
            'data/groups.xml',
            'views/project_view.xml',
            'views/manufacturing.xml',
            'wizard/views/create_project_view.xml'
         ],

    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
