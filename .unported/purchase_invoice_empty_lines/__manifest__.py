# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Purchase Invoice Empty Lines",
    'summary': "Add a button to empty the lines from a draft supplier invoice",
    'author': "Numigi",
    'maintainer': "Numigi",
    'website': "https://bit.ly/numigi-com",
    'licence': "AGPL-3",
    'version': '1.0.0',
    'depends': ['purchase'],
    'data': [
        "views/account_invoice.xml",
    ],
    'installable': True,
}
