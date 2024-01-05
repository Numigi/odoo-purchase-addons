# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import threading
from odoo import models, fields, exceptions, _
from odoo.addons.product_supplier_info_helpers.helpers import get_supplier_info_from_product


def is_testing():
    """Return whether the unit tests are being ran."""
    return getattr(threading.currentThread(), 'testing', False)


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    commercial_partner_id = fields.Many2one(
        "res.partner", related="partner_id.commercial_partner_id")

    def _check_product_sellers(self):
        expected_supplier = self.partner_id.commercial_partner_id

        for line in self.order_line:
            supplier_info = get_supplier_info_from_product(line.product_id)
            authorized_suppliers = supplier_info.mapped('name.commercial_partner_id')
            if expected_supplier not in authorized_suppliers:
                raise exceptions.ValidationError(_(
                    "The product {product} is not allowed for the supplier {supplier}.\n"
                    "Please contact your manager."
                ).format(
                    product=line.product_id.display_name,
                    supplier=expected_supplier.display_name,
                ))

    def button_confirm(self):
        constraint_should_be_executed = (
            not is_testing() or self._context.get('force_apply_purchase_partner_products')
        )
        if constraint_should_be_executed:
            for order in self:
                order._check_product_sellers()
        return super().button_confirm()


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    commercial_partner_id = fields.Many2one(
        "res.partner", related="order_id.commercial_partner_id")
