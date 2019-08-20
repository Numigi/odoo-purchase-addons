# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, exceptions, _


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    commercial_partner_id = fields.Many2one(
        "res.partner", related="partner_id.commercial_partner_id")

    def _check_product_sellers(self):
        expected_supplier = self.partner_id.commercial_partner_id

        for line in self.order_line:
            authorized_suppliers = line.mapped('product_id.seller_ids.name.commercial_partner_id')

            if expected_supplier not in authorized_suppliers:
                raise exceptions.ValidationError(_(
                    "The product {product} is not allowed for the supplier {supplier}.\n"
                    "Please contact your manager."
                ).format(
                    product=line.product_id.display_name,
                    supplier=expected_supplier.display_name,
                ))

    @api.multi
    def button_confirm(self):
        for order in self:
            order._check_product_sellers()
        return super().button_confirm()


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    commercial_partner_id = fields.Many2one(
        "res.partner", related="order_id.commercial_partner_id")
