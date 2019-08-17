# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Purchase partner products",

    'summary': """
        Restriction selection articles on PO""",

    'author': "Numigi",
    'maintainer': "Numigi",
    'website': "https://bit.ly/numigi-com",
    'licence': "AGPL-3",

    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase'],

    # always loaded
    'data': [
        "views/purchase_view.xml",

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
