# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.addons.product_supplier_info_helpers.helpers import (
    get_products_from_supplier_info,
    get_supplier_info_from_product,
)


def _propagate_consignment_from_category(product):
    product.consignment = product.categ_id.consignment


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    consignment = fields.Boolean(
        help="If checked, only one supplier can be selected in the supplier prices list "
        "for this product. "
        "The supplier will automatically be set as owner of the stock "
        "on receipt orders."
    )

    @api.onchange('categ_id')
    def _onchange_category_set_consignment(self):
        _propagate_consignment_from_category(self)

    @api.constrains('consignment')
    def _check_single_consigned_vendor_if_consigned(self):
        self.mapped('product_variant_ids')._check_single_consigned_vendor_if_consigned()


class Product(models.Model):

    _inherit = 'product.product'

    @api.onchange('categ_id')
    def _onchange_category_set_consignment(self):
        _propagate_consignment_from_category(self)

    def _check_single_consignment_vendor(self):
        supplier_info = get_supplier_info_from_product(self)
        vendors = supplier_info.mapped('name.commercial_partner_id')
        if len(vendors) > 1:
            raise ValidationError(_(
                'The product {product} is consigned. '
                'Therefore, you may not select more than one different vendor '
                'on this product. The following vendors were selected:\n'
                ' * {vendors}'
            ).format(
                product=self.display_name,
                vendors='\n * '.join(vendors.mapped('display_name'))
            ))

    @api.constrains('consignment')
    def _check_single_consigned_vendor_if_consigned(self):
        products_with_consignment = self.filtered(lambda p: p.consignment)
        for product in products_with_consignment:
            product._check_single_consignment_vendor()


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
