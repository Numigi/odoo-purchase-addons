# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase
from ..helpers import get_products_from_supplier_info, get_supplier_info_from_product


class TestSupplierInfoHelpers(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier_1 = cls.env["res.partner"].create(
            {"name": "Supplier 1", "supplier": True}
        )
        cls.supplier_2 = cls.env["res.partner"].create(
            {"name": "Supplier 2", "supplier": True}
        )

        cls.template_a = cls.env["product.template"].create(
            {"name": "Product Template A"}
        )

        cls.variant_a1 = cls.env["product.product"].create(
            {"name": "Variant A1", "product_tmpl_id": cls.template_a.id}
        )

        cls.variant_a2 = cls.env["product.product"].create(
            {"name": "Variant A2", "product_tmpl_id": cls.template_a.id}
        )

    def _create_supplier_info(self, supplier, template=None, variant=None):
        return self.env["product.supplierinfo"].create(
            {
                "product_id": variant.id if variant else None,
                "product_tmpl_id": template.id
                if template
                else variant.product_tmpl_id.id,
                "name": supplier.id,
            }
        )

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
