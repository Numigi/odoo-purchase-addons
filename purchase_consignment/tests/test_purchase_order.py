# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestPropagationOfPartnerToStockMove(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env['res.partner'].create({
            'name': 'Supplier',
            'supplier': True,
        })

        cls.product = cls.env['product.product'].create({
            'name': 'Product A',
            'type': 'product',
            'consignment': True,
            'seller_ids': [(0, 0, {'name': cls.supplier.id})],
        })

        cls.order = cls.env['purchase.order'].create({
            'partner_id': cls.supplier.id,
            'order_line': [(0, 0, {
                'product_id': cls.product.id,
                'product_uom': cls.product.uom_id.id,
                'name': cls.product.name,
                'product_qty': 1,
                'price_unit': 100,
                'date_planned': datetime.now(),
            })]
        })

    def test_after_confirmed__stock_move_owner_is_the_supplier(self):
        self.order.button_confirm()
        move_line = self.order.picking_ids.move_lines.move_line_ids
        assert move_line.owner_id == self.supplier

    def test_if_not_consigned__after_confirmed__stock_move_owner_not_set(self):
        self.product.consignment = False
        self.order.button_confirm()
        move_line = self.order.picking_ids.move_lines.move_line_ids
        assert not move_line.owner_id

    def test_if_po_has_wrong_supplier__constraint_raised(self):
        self.order.partner_id = self.supplier.copy()
        with pytest.raises(ValidationError):
            self.order.button_confirm()
