# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Purchase Consignment / Inventory",
    'summary': "Inventory adjustments based on consignment owners",
    'author': "Numigi",
    'maintainer': "Numigi",
    'website': "https://bit.ly/numigi-com",
    'licence': "AGPL-3",
    'version': '1.0.1',
    'depends': [
        'purchase_consignment',
    ],
    'data': [
        "views/stock_inventory.xml",
    ],
    'installable': True,
}
