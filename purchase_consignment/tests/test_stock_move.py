# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestStockMoveOwner(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env["res.partner"].create(
            {"name": "Supplier", "supplier": True}
        )

        cls.category = cls.env["product.category"].create(
            {"name": "Consignment", "consignment": True}
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Product A",
                "type": "product",
                "categ_id": cls.category.id,
                "seller_ids": [(0, 0, {"name": cls.supplier.id})],
            }
        )

        cls.supplier_location = cls.env.ref("stock.stock_location_suppliers")
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.internal_location = cls.warehouse.lot_stock_id

    def test_onchange_product__owner_automatically_set(self):
        vals = {
            "product_id": self.product.id,
            "location_id": self.supplier_location.id,
            "location_dest_id": self.internal_location.id,
        }
        result = self.env["stock.move.line"].play_onchanges(vals, ["product_id"])
        assert result["owner_id"] == self.supplier.id

    def test_prepare_stock_move_line_vals(self):
        stock_move = self.env["stock.move"].create(
            {
                "name": "/",
                "product_id": self.product.id,
                "product_uom": self.product.uom_id.id,
                "location_id": self.supplier_location.id,
                "location_dest_id": self.internal_location.id,
            }
        )
        result = stock_move._prepare_move_line_vals()
        assert result["owner_id"] == self.supplier.id
