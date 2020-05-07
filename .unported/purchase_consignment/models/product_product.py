# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError
from odoo.addons.product_supplier_info_helpers.helpers import (
    get_supplier_info_from_product,
)


class Product(models.Model):

    _inherit = "product.product"

    @api.constrains("consignment")
    def _check_single_consigned_vendor_if_consigned(self):
        products_with_consignment = self.filtered(lambda p: p.consignment)
        for product in products_with_consignment:
            product._check_single_consignment_vendor()

    def _check_single_consignment_vendor(self):
        supplier_info = get_supplier_info_from_product(self)
        vendors = supplier_info.mapped("name.commercial_partner_id")
        if len(vendors) > 1:
            raise ValidationError(
                _(
                    "The product {product} is consigned. "
                    "Therefore, you may not select more than one different vendor "
                    "on this product. The following vendors were selected:\n"
                    " * {vendors}"
                ).format(
                    product=self.display_name,
                    vendors="\n * ".join(vendors.mapped("display_name")),
                )
            )
