# © 2019 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Main Module',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Install all addons required for testing.',
    'depends': [
        'product_supplier_info_helpers',
        'purchase_consignment',
        'purchase_consignment_delivery_expense',
        'purchase_consignment_inventory',
        'purchase_estimated_time_arrival',
        'purchase_invoice_empty_lines',
        'purchase_invoice_from_picking',
        'purchase_partner_products',
        'purchase_warning_minimum_amount',
    ],
    'installable': True,
}
