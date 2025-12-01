# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    """
    Inherit purchase.order model to add supplier warning validation
    """
    _inherit = 'purchase.order'

    @api.onchange('partner_id')
    def onchange_partner_id_warning(self):
        return

    def button_confirm(self):
        """
        Override the confirm button to check for supplier warnings
        Displays a confirmation wizard if supplier has warnings
        """
        # Check if we should bypass supplier warning (after wizard confirmation)
        if self.env.context.get('bypass_supplier_warning'):
            return super(PurchaseOrder, self).button_confirm()

        # Check for supplier warnings on each purchase order
        for order in self:
            supplier = order.partner_id

            # Check if supplier has a blocking warning
            if supplier.purchase_warn == 'block' and supplier.purchase_warn_msg:
                raise UserError(supplier.purchase_warn_msg)

            # Check if supplier has a warning message configured
            if (supplier.purchase_warn == 'warning'
                    and supplier.purchase_warn_msg
                    and not self.env.context.get('suppress_supplier_warning')):
                # Open confirmation wizard with supplier warning
                return self._open_confirmation_wizard(order, supplier)

        # Standard behavior if no warnings found
        return super(PurchaseOrder, self).button_confirm()

    def _open_confirmation_wizard(self, purchase_order, supplier):
        """
        Open the confirmation wizard with supplier warning message

        Args:
            purchase_order (purchase.order): Purchase order being validated
            supplier (res.partner): Supplier with warning message

        Returns:
            dict: Wizard action to open confirmation dialog
        """
        # Return wizard action
        title = _("Warning for %s", supplier.name)
        message = supplier.purchase_warn_msg
        return {
            'name': title,
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.confirmation.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref(
                'purchase_order_confirm_warning.confirmation_wizard_view_form'
            ).id,
            'target': 'new',
            'context': {
                'default_warning_message': message,
                'default_purchase_order_id': purchase_order.id
            }
        }
