# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Purchase Partner Products",
    'summary': "Restrict product selection on purchase orders",
    'author': "Numigi",
    'maintainer': "Numigi",
    'website': "https://bit.ly/numigi-com",
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
