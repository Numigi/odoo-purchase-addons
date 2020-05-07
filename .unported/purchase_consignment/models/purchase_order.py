# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError
from odoo.addons.product_supplier_info_helpers.helpers import (
    get_supplier_info_from_product,
)


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    @api.multi
    def button_confirm(self):
        lines_with_consignment = self.mapped("order_line").filtered(
            lambda l: l.product_id.consignment
        )
        for line in lines_with_consignment:
            line._check_product_consignment_vendor()
        return super().button_confirm()


class PurchaseOrderLine(models.Model):

    _inherit = "purchase.order.line"

    def _check_product_consignment_vendor(self):
        """Check that the vendor defined on product is the vendor on the PO.

        The commercial partner must be defined in the list of prices for the product.
        """
        supplier_info = get_supplier_info_from_product(self.product_id)
        vendors_on_product = supplier_info.mapped("name.commercial_partner_id")
        vendor_on_po = self.order_id.partner_id.commercial_partner_id

        if vendor_on_po not in vendors_on_product:
            raise ValidationError(
                _(
                    "The purchase order {order} can not be confirmed because "
                    "the supplier {supplier} defined on the PO is absent from "
                    "the list of suppliers for the consigned product {product}."
                ).format(
                    order=self.order_id.display_name,
                    supplier=vendor_on_po.display_name,
                    product=self.product_id.display_name,
                )
            )
