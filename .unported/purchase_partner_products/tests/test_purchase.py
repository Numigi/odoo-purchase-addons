# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestPurchaseOrder(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_1 = cls.env["res.partner"].create(
            {"name": "My Partner Company 1", "supplier": True, "is_company": True}
        )
        cls.contact_1 = cls.env["res.partner"].create(
            {
                "name": "My Contact 1",
                "supplier": True,
                "is_company": False,
                "parent_id": cls.partner_1.id,
            }
        )

        cls.partner_2 = cls.env["res.partner"].create(
            {"name": "My Partner Company 2", "supplier": True, "is_company": True}
        )

        cls.product_categ = cls.env.ref("product.product_category_5")
        cls.uom_unit = cls.env.ref("product.product_uom_unit")

        cls.product_1 = cls.env["product.product"].create(
            cls._get_product_vals(cls.partner_1)
        )
        cls.product_2 = cls.env["product.product"].create(
            cls._get_product_vals(cls.partner_2)
        )

        cls.order = cls.env["purchase.order"].create(
            {"partner_id": cls.partner_1.id, "order_line": []}
        )

    @classmethod
    def _get_product_vals(cls, suppliers):
        return {
            "name": "Acier Lac 3.4",
            "categ_id": cls.product_categ.id,
            "type": "consu",
            "uom_id": cls.uom_unit.id,
            "uom_po_id": cls.uom_unit.id,
            "default_code": "ACIERLC3",
            "seller_ids": [(0, 0, {"name": p.id}) for p in suppliers],
        }

    @classmethod
    def _get_po_line_vals(cls, product):
        return {
            "name": product.name,
            "product_id": product.id,
            "product_qty": 6.0,
            "product_uom": product.uom_po_id.id,
            "price_unit": 100.0,
            "date_planned": datetime.now(),
        }

    def confirm_order(self):
        self.order.with_context(
            force_apply_purchase_partner_products=True
        ).button_confirm()

    def test_if_one_product_with_same_partner__error_not_raised(self):
        self.order.write(
            {"order_line": [(0, 0, self._get_po_line_vals(self.product_1))]}
        )
        self.confirm_order()

    def test_if_two_products_with_same_partner__error_not_raised(self):
        self.order.write(
            {
                "order_line": [
                    (0, 0, self._get_po_line_vals(self.product_1)),
                    (0, 0, self._get_po_line_vals(self.product_1)),
                ]
            }
        )
        self.confirm_order()

    def test_if_one_product_with_child_partner__error_not_raised(self):
        self.order.write(
            {"order_line": [(0, 0, self._get_po_line_vals(self.product_1))]}
        )
        self.order.partner_id = self.contact_1
        self.confirm_order()

    def test_if_one_product_unrelated_partner__error_raised(self):
        self.order.write(
            {"order_line": [(0, 0, self._get_po_line_vals(self.product_2))]}
        )
        with pytest.raises(ValidationError):
            self.confirm_order()

    def test_if_partner_defined_on_variant__error_raised(self):
        template = self.product_1.product_tmpl_id

        self.product_1.copy({"product_tmpl_id": template.id})
        template.seller_ids.product_id = self.product_1

        self.order.write(
            {"order_line": [(0, 0, self._get_po_line_vals(self.product_1))]}
        )
        self.confirm_order()

    def test_if_partner_defined_on_other_variant__error_raised(self):
        template = self.product_1.product_tmpl_id

        other_variant = self.product_1.copy({"product_tmpl_id": template.id})
        template.seller_ids.product_id = other_variant

        self.order.write(
            {"order_line": [(0, 0, self._get_po_line_vals(self.product_1))]}
        )

        with pytest.raises(ValidationError):
            self.confirm_order()
