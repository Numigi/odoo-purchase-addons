# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    consignment = fields.Boolean(
        related="categ_id.consignment",
        store=True,
        help="If checked, only one supplier can be selected in the supplier prices list "
        "for this product. "
        "The supplier will automatically be set as owner of the stock "
        "on receipt orders.",
    )

    @api.constrains("consignment")
    def _check_single_consigned_vendor_if_consigned(self):
        self.mapped("product_variant_ids")._check_single_consigned_vendor_if_consigned()
