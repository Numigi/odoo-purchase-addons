# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Purchase Order Confirmation Wizard',
    'version': '14.0.1.0.0',
    'category': 'Purchases',
    'summary': 'Confirmation wizard with supplier warnings for purchase order validation',
    'description': """
        Purchase Order Confirmation Wizard

        This module adds a confirmation wizard that displays supplier warnings
        when validating purchase orders.

        Key Features :
        - Displays supplier warning messages during purchase order validation
        - Provides explicit user confirmation for orders with supplier warnings
        - Non-blocking interface that allows users to proceed or cancel validation
        - Maintains standard Odoo behavior for suppliers without warnings

        Usage:
        When validating a purchase order for a supplier with configured warnings,
        a confirmation wizard appears showing the warning message. The user can
        choose to proceed with validation or cancel the operation.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/purchase_confirmation_wizard.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
