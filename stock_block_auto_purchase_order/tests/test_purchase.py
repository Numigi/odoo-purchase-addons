# © 2018 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestPurchase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "tname"})
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.rule = cls.warehouse.buy_pull_id

    def test_make_po_get_domain(self):
        domain = self.rule._make_po_get_domain(
            {
                "company_id": self.env.user.company_id,
                "picking_type_id": self.warehouse.in_type_id,
            },
            self.partner,
        )
        assert ("block_auto_purchase_order", "=", False) in domain


class TestProductCategories(common.SavepointCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].new({})

        self.product = self.env["product.product"].new({})

        self.order = self.env["purchase.order"].new({})
        self.order.partner_id = self.partner

        self.line = self.env["purchase.order.line"].new({})
        self.line.product_id = self.product

        self.order.order_line = self.line

    def test_product_with_automatic_block(self):
        self.product.block_auto_purchase_order = True
        self.order.onchange_lines_set_automatic_block()
        assert self.order.block_auto_purchase_order

    def test_product_without_automatic_block(self):
        self.order.onchange_lines_set_automatic_block()
        assert not self.order.block_auto_purchase_order

    def test_box_checked_manually_on_purchase_order(self):
        self.order.block_auto_purchase_order = True
        self.order.onchange_lines_set_automatic_block()
        assert self.order.block_auto_purchase_order
