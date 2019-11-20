# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Purchase Estimated Time of Arrival (ETA)",
    'summary': "Compute the estimated time of arrival of purchased products",
    'author': "Numigi",
    'maintainer': "Numigi",
    'website': "https://bit.ly/numigi-com",
    'licence': "AGPL-3",
    'version': '1.0.0',
    'depends': ['purchase_stock'],
    'data': [
        "views/product.xml",
        "views/purchase_order.xml",
        "views/res_config_settings.xml",
        "views/stock_arrival_time.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
}
