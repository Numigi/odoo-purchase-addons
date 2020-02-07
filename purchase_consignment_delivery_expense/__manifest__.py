# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Purchase Consignment Delivery Expense",
    'summary': "Generate journal entries on delivery of consigned products.",
    'author': "Numigi",
    'maintainer': "Numigi",
    'website': "https://bit.ly/numigi-com",
    'licence': "AGPL-3",
    'version': '1.0.0',
    'depends': [
        'purchase_consignment',
    ],
    'data': [
        "views/product_category.xml",
    ],
    'installable': True,
}
