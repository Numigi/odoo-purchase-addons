# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Purchase Partner Products",
    'summary': "Restrict product selection on purchase orders",
    'author': "Numigi",
    'maintainer': "Numigi",
    'website': "https://numigi.com/r/home",
    'licence': "AGPL-3",
    'version': '1.2.1',
    'depends': [
        'purchase',
        'product_supplier_info_helpers',
    ],
    'data': [
        "views/purchase_view.xml",
    ],
    'installable': True,
}
