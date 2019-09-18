# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestInventoryByOwner(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env['res.partner'].create({
            'name': 'Supplier',
            'supplier': True,
        })

        cls.warehouse = cls.env['stock.warehouse'].create({
            'name': 'My Warehouse',
            'code': 'MYWH',
        })

        cls.stock_location = cls.warehouse.lot_stock_id

        cls.child_location = cls.env['stock.location'].create({
            'name': 'Child Location',
            'location_id': cls.warehouse.lot_stock_id.id,
            'usage': 'internal',
        })

        cls.product_a = cls.env['product.product'].create({
            'name': 'Product A',
            'type': 'product',
            'consignment': True,
            'seller_ids': [(0, 0, {'name': cls.supplier.id})],
        })

        cls.product_b = cls.env['product.product'].create({
            'name': 'Product B',
            'type': 'product',
            'consignment': True,
            'seller_ids': [(0, 0, {'name': cls.supplier.id})],
        })

        cls.inventory = cls.env['stock.inventory'].create({
            'name': 'Consignment Inventory',
            'filter': 'consignment',
            'location_id': cls.stock_location.id,
            'consignment_supplier_id': cls.supplier.id,
            'exhausted': False,
        })

    def _add_quant(self, product, quantity, location=None, owner=None, lot=None, package=None):
        self.env['stock.quant'].create({
            'product_id': product.id,
            'location_id': (location or self.stock_location).id,
            'quantity': quantity,
            'owner_id': owner.id if owner else None,
            'lot_id': lot.id if lot else None,
            'package_id': package.id if package else None,
        })

    def test_if_enable_exhausted__one_line_created_per_product(self):
        self.inventory.exhausted = True
        self.inventory.action_start()
        lines = self.inventory.line_ids
        assert len(lines) == 2
        assert lines[0].product_id == self.product_a
        assert lines[1].product_id == self.product_b

    def test_owner_automatically_set_on_exhausted_line(self):
        self.inventory.exhausted = True
        self.inventory.action_start()
        lines = self.inventory.line_ids
        assert len(lines) == 2
        for line in lines:
            assert line.partner_id == self.supplier

    def test_exhausted_not_enabled_and_no_quant__no_lines_shown(self):
        self.inventory.action_start()
        assert not self.inventory.line_ids

    def test_exhausted_not_enabled_and_one_quant__one_line_created(self):
        self._add_quant(self.product_a, 1)
        self.inventory.action_start()
        lines = self.inventory.line_ids
        assert len(lines) == 1
        assert lines[0].product_id == self.product_a

    def test_exhausted_enabled_and_one_quant__one_line_created_per_product(self):
        self.inventory.exhausted = True
        self._add_quant(self.product_a, 1)
        self.inventory.action_start()
        lines = self.inventory.line_ids
        assert len(lines) == 2
        assert lines[0].product_id == self.product_a
        assert lines[1].product_id == self.product_b

    def test_owner_mapped_properly_from_quant(self):
        expected_owner = self.env['res.partner'].create({'name': 'Other Supplier'})
        self._add_quant(self.product_a, 1, owner=expected_owner)
        self.inventory.action_start()
        assert self.inventory.line_ids.partner_id == expected_owner

    def test_inventory_lines_grouped_per_quant_owner(self):
        owner_1 = self.env['res.partner'].create({'name': 'Owner 1'})
        owner_2 = self.env['res.partner'].create({'name': 'Owner 2'})
        self._add_quant(self.product_a, 1, owner=owner_1)
        self._add_quant(self.product_a, 2, owner=owner_1)
        self._add_quant(self.product_a, 4, owner=owner_2)
        self.inventory.action_start()
        lines = sorted(self.inventory.line_ids, key=lambda l: l.partner_id.id)
        assert len(lines) == 2
        assert lines[0].partner_id == owner_1
        assert lines[0].theoretical_qty == 3  # 1 + 2
        assert lines[1].partner_id == owner_2
        assert lines[1].theoretical_qty == 4

    def test_inventory_lines_grouped_per_production_lot(self):
        self.product_a.tracking = 'lot'
        lot_1 = self.env['stock.production.lot'].create({
            'name': 'Lot 1', 'product_id': self.product_a.id
        })
        lot_2 = self.env['stock.production.lot'].create({
            'name': 'Lot 2', 'product_id': self.product_a.id
        })
        self._add_quant(self.product_a, 1, lot=lot_1)
        self._add_quant(self.product_a, 2, lot=lot_1)
        self._add_quant(self.product_a, 4, lot=lot_2)
        self.inventory.action_start()
        lines = sorted(self.inventory.line_ids, key=lambda l: l.prod_lot_id.id)
        assert len(lines) == 2
        assert lines[0].prod_lot_id == lot_1
        assert lines[0].theoretical_qty == 3  # 1 + 2
        assert lines[1].prod_lot_id == lot_2
        assert lines[1].theoretical_qty == 4

    def test_inventory_lines_grouped_per_package(self):
        package_1 = self.env['stock.quant.package'].create({
            'name': 'Package 1',
        })
        package_2 = self.env['stock.quant.package'].create({
            'name': 'Package 2',
        })
        self._add_quant(self.product_a, 1, package=package_1)
        self._add_quant(self.product_a, 2, package=package_1)
        self._add_quant(self.product_a, 4, package=package_2)
        self.inventory.action_start()
        lines = sorted(self.inventory.line_ids, key=lambda l: l.package_id.id)
        assert len(lines) == 2
        assert lines[0].package_id == package_1
        assert lines[0].theoretical_qty == 3  # 1 + 2
        assert lines[1].package_id == package_2
        assert lines[1].theoretical_qty == 4

    def test_inventory_lines_grouped_per_location(self):
        location_1 = self.stock_location
        location_2 = self.child_location
        self._add_quant(self.product_a, 1, location=location_1)
        self._add_quant(self.product_a, 2, location=location_1)
        self._add_quant(self.product_a, 4, location=location_2)
        self.inventory.action_start()
        lines = sorted(self.inventory.line_ids, key=lambda l: l.location_id.id)
        assert len(lines) == 2
        assert lines[0].location_id == location_1
        assert lines[0].theoretical_qty == 3  # 1 + 2
        assert lines[1].location_id == location_2
        assert lines[1].theoretical_qty == 4
