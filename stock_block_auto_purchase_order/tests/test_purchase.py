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
        self.assertIn(("block_auto_purchase_order", "=", False), domain)
