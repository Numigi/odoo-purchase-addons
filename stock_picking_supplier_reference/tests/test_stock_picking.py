# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from datetime import datetime
from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError
from uuid import uuid4


class TestSearchPickingWithInvoiceContext(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.user.company_id

        cls.supplier_reference = str(uuid4())

        cls.supplier = cls.env["res.partner"].create(
            {"name": "Supplier", "supplier": True}
        )

        cls.product_a = cls.env["product.product"].create(
            {"name": "Product A", "type": "product"}
        )

        cls.order = cls.env["purchase.order"].create(
            {
                "partner_id": cls.supplier.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_a.id,
                            "product_uom": cls.product_a.uom_po_id.id,
                            "name": cls.product_a.name,
                            "product_qty": 10,
                            "price_unit": 100,
                            "date_planned": datetime.now(),
                        },
                    )
                ],
            }
        )
        cls.order.button_confirm()
        cls.picking = cls.order.picking_ids
        cls.picking.supplier_reference = cls.supplier_reference

        cls.picking_obj = cls.env["stock.picking"]
        cls.picking_obj_with_context = cls.picking_obj.with_context(
            show_picking_supplier_reference=True
        )

    def test_if_supplier_reference_context__reference_in_display_name(self):
        result = self.picking_obj_with_context.name_search(self.supplier_reference)
        assert len(result) == 1
        assert result[0][0] == self.picking.id
        assert self.supplier_reference in result[0][1]

    def test_if_not_supplier_reference_context__reference_not_in_display_name(self):
        result = self.picking_obj.name_search(self.supplier_reference)
        assert len(result) == 1
        assert result[0][0] == self.picking.id
        assert self.supplier_reference not in result[0][1]

    def test_if_picking_has_origin__origin_in_display_name(self):
        origin = str(uuid4)
        self.picking.origin = origin
        result = self.picking_obj_with_context.name_search(self.supplier_reference)
        assert len(result) == 1
        assert result[0][0] == self.picking.id
        assert origin in result[0][1]

    def test_2_pickings_with_same_reference__no_constraint(self):
        new_picking = self.picking.copy()
        new_picking.supplier_reference = self.supplier_reference

    def test_2_pickings_with_same_reference__unique_constraint(self):
        self.company.unique_picking_supplier_reference = True
        new_picking = self.picking.copy()
        with pytest.raises(ValidationError):
            new_picking.supplier_reference = self.supplier_reference
