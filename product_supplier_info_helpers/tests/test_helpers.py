# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase, tagged
from ..helpers import (
    get_products_from_supplier_info,
    get_supplier_info_from_product,
)


@tagged('post_install')
class TestSupplierInfoHelpers(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier_1 = cls.env['res.partner'].create({
            'name': 'Supplier 1'
        })
        cls.supplier_2 = cls.env['res.partner'].create({
            'name': 'Supplier 2'
        })
        product_attribute = cls.env['product.attribute'].create({'name': 'Size'})
        size_value_l = cls.env['product.attribute.value'].create([{
            'name': 'L',
            'attribute_id': product_attribute.id,
        }])
        size_value_s = cls.env['product.attribute.value'].create([{
            'name': 'S',
            'attribute_id': product_attribute.id,
        }])

        cls.template_a = cls.env['product.template'].create({
            'name': 'Product Template A',
        })
        ptal = cls.env['product.template.attribute.line'].create({
            'attribute_id': product_attribute.id,
            'product_tmpl_id': cls.template_a.id,
            'value_ids': [(6, 0, [size_value_s.id, size_value_l.id])],
        })
        cls.variant_a1 = cls.template_a.product_variant_ids[0]
        cls.variant_a2 = cls.template_a.product_variant_ids[1]

    def _create_supplier_info(self, supplier, template=None, variant=None):
        return self.env['product.supplierinfo'].create({
            'product_id': variant.id if variant else None,
            'product_tmpl_id': template.id if template else variant.product_tmpl_id.id,
            'name': supplier.id,
        })

    def test_if_specific_to_variant__info_mapped_from_product(self):
        info = self._create_supplier_info(self.supplier_1, variant=self.variant_a1)
        assert info in get_supplier_info_from_product(self.variant_a1)

    def test_if_specific_to_other_variant__info_not_mapped_from_product(self):
        info = self._create_supplier_info(self.supplier_1, variant=self.variant_a2)
        assert info not in get_supplier_info_from_product(self.variant_a1)

    def test_if_generic_on_template__info_mapped_from_product(self):
        info = self._create_supplier_info(self.supplier_1, template=self.template_a)
        assert info in get_supplier_info_from_product(self.variant_a1)

    def test_if_specific_to_variant__product_mapped_from_info(self):
        info = self._create_supplier_info(self.supplier_1, variant=self.variant_a1)
        assert self.variant_a1 in get_products_from_supplier_info(info)

    def test_if_specific_to_other_variant__product_mapped_from_info(self):
        info = self._create_supplier_info(self.supplier_1, variant=self.variant_a2)
        assert self.variant_a1 not in get_products_from_supplier_info(info)

    def test_if_generic_on_template__product_mapped_from_info(self):
        info = self._create_supplier_info(self.supplier_1, template=self.template_a)
        assert self.variant_a1 in get_products_from_supplier_info(info)
