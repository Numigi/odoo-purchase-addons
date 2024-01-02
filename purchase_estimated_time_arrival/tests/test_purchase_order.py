# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo.tests import Form
from odoo.tests.common import SavepointCase


class TestPurchaseOrder(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env["res.partner"].create(
            {
                "name": "Supplier",
            }
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Product A",
                "type": "product",
            }
        )

        cls.order = cls.env["purchase.order"].create(
            {
                "partner_id": cls.supplier.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom": cls.product.uom_id.id,
                            "name": cls.product.name,
                            "product_qty": 1,
                            "price_unit": 100,
                            # The planned date is not used to compute the ETA.
                            "date_planned": datetime.now() + timedelta(9999),
                        },
                    )
                ],
            }
        )

        cls.order = cls.order.sudo(cls.env.ref("base.user_demo"))
        cls.order_line = cls.order.order_line

    @staticmethod
    def _process_picking(picking):
        for move_line in picking.mapped("move_lines.move_line_ids"):
            move_line.qty_done = move_line.product_uom_qty
        picking.button_validate()

    def _return_picking(self, picking):
        return_form = Form(
            self.env["stock.return.picking"].with_context(
                active_id=picking.id, active_model="stock.picking"
            )
        )
        return_wizard = return_form.save()
        picking_id, pick_type_id = return_wizard._create_returns()
        return_picking = self.env["stock.picking"].browse(picking_id)
        self._process_picking(return_picking)
        return return_picking

    def _get_eta_records(self):
        return self.env["stock.arrival.time"].search(
            [
                ("product_id", "=", self.product.id),
            ]
        )

    def test_after_picking_processed_one_eta_line_generated(self):
        self.order.button_confirm()
        self._process_picking(self.order.picking_ids)
        assert len(self._get_eta_records()) == 1

    def test_eta_days_is__receipt_date__minus__purchase_date(self):
        expected_days = 3
        self.order.date_order = datetime.now() - timedelta(expected_days)
        self.order.button_confirm()
        self._process_picking(self.order.picking_ids)
        eta_line = self._get_eta_records()
        assert round(eta_line.days, 2) == expected_days

    def test_on_stock_return__no_extra_eta_line_generated(self):
        self.order.button_confirm()
        self._process_picking(self.order.picking_ids)
        self._return_picking(self.order.picking_ids)
        assert len(self._get_eta_records()) == 1
