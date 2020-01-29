# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.addons.product_supplier_info_helpers.helpers import (
    get_products_from_supplier_info,
)


class ProductSupplierInfo(models.Model):

    _inherit = 'product.supplierinfo'

    def _check_single_consigned_vendor(self):
        products = get_products_from_supplier_info(self)
        products._check_single_consigned_vendor_if_consigned()

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res._check_single_consigned_vendor()
        return res

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        self._check_single_consigned_vendor()
        return res
