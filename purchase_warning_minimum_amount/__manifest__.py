# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-v3).

{
    'name': "Purchase Warning Minimum Amount",

    'summary': """
        Management minimum Supplier Order
        """,

    'author': "Numigi",
    'maintainer': "Numigi",
    'website': "https://bit.ly/numigi-com",
    'licence': "AGPL-3",

    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase'],

    # always loaded
    'data': [
        'views/partner_view.xml',
        'views/purchase_view.xml',
        'wizard/wizard_alert_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
