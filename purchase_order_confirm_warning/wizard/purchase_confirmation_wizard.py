# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class PurchaseConfirmationWizard(models.TransientModel):
    """
    Confirmation Wizard for Purchase Orders with Supplier Warnings
    Displays supplier warnings and allows user to confirm or cancel the
    purchase order validation
    """
    _name = 'purchase.confirmation.wizard'
    _description = 'Purchase Order Confirmation Wizard with Supplier Warning'

    warning_message = fields.Text(
        string='Warning Message',
        readonly=True,
        help='Supplier warning message to display to the user'
    )

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        readonly=True,
        help='Purchase order being validated'
    )

    def action_confirm_validation(self):
        """
        Confirm purchase order validation after user approval
        Bypasses the supplier warning check and proceeds with normal validation
        """
        self.ensure_one()

        # Confirm purchase order with context to bypass warning check
        return self.purchase_order_id.with_context(
            bypass_supplier_warning=True
        ).button_confirm()
