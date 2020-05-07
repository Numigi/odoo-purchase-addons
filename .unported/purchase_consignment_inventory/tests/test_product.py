# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestNameSearch(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = cls.env["product.category"].create(
            {"name": "Consignment", "consignment": True}
        )

        cls.supplier_a = cls.env["res.partner"].create(
            {"name": "Supplier A", "supplier": True}
        )

        cls.supplier_b = cls.env["res.partner"].create(
            {"name": "Supplier A", "supplier": True}
        )

        cls.product_a1 = cls.env["product.product"].create(
            {
                "name": "Product A1",
                "type": "product",
                "categ_id": cls.category.id,
                "seller_ids": [(0, 0, {"name": cls.supplier_a.id})],
            }
        )

        cls.product_a2 = cls.env["product.product"].create(
            {
                "name": "Product A2",
                "type": "product",
                "categ_id": cls.category.id,
                "seller_ids": [(0, 0, {"name": cls.supplier_a.id})],
            }
        )

        cls.product_b1 = cls.env["product.product"].create(
            {
                "name": "Product B1",
                "type": "product",
                "categ_id": cls.category.id,
                "seller_ids": [(0, 0, {"name": cls.supplier_b.id})],
            }
        )

    def _search(self, name: str, supplier: "ResPartner" = None):
        product_obj = self.env["product.product"].with_context(
            filter_products_by_consignment_supplier=(True if supplier else False),
            consignment_supplier_id=(supplier.id if supplier else None),
        )
        return product_obj.name_search(name, limit=None)

    def test_if_filter_by_vendor__products_filtered(self):
        result = self._search("1", self.supplier_a)
        assert result == [(self.product_a1.id, self.product_a1.display_name)]

    def test_if_not_filter_by_vendor__products_not_filtered(self):
        result = self._search("1")
        product_ids = [p[0] for p in result]
        assert self.product_a1.id in product_ids
        assert self.product_b1.id in product_ids
