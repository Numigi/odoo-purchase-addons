# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from .common import StockInventoryCase


class TestOwner(StockInventoryCase):

    def test_if_product_has_supplier__error_not_raised(self):
        self._start_inventory_with_owner(self.supplier_a)
        self.inventory.line_ids = self._new_inventory_line(self.product_a, owner=self.supplier_a)
        self.inventory.action_validate()

    def test_if_product_has_not_supplier__raise_error(self):
        self._start_inventory_with_owner(self.supplier_a)
        self.inventory.line_ids = self._new_inventory_line(self.product_a, owner=self.supplier_a)
        self.product_a.seller_ids.unlink()

        with pytest.raises(ValidationError):
            self.inventory.action_validate()

    def test_if_supplier_not_selected__raise_error(self):
        self._start_inventory_with_owner(self.supplier_a)
        self.inventory.line_ids = self._new_inventory_line(self.product_a, owner=None)

        with pytest.raises(ValidationError):
            self.inventory.action_validate()

    def test_if_wrong_supplier_selected__raise_error(self):
        self._start_inventory_with_owner(self.supplier_a)

        wrong_supplier = self.supplier_a.copy({'name': 'Wrong Supplier'})
        self.inventory.line_ids = self._new_inventory_line(self.product_a, owner=wrong_supplier)

        with pytest.raises(ValidationError):
            self.inventory.action_validate()

    def test_if_child_supplier_in_supplier_prices__error_not_raised(self):
        self._start_inventory_with_owner(self.supplier_a)
        self.product_a.seller_ids.name = self.supplier_a_contact
        self.inventory.line_ids = self._new_inventory_line(
            self.product_a, owner=self.supplier_a)
        self.inventory.action_validate()

    def _start_inventory_with_owner(self, owner):
        self.inventory.write({
            'partner_id': owner.id,
            'filter': 'owner',
        })
        self.inventory.action_start()

    def _new_inventory_line(self, product, owner=None):
        return self.env['stock.inventory.line'].new({
            'partner_id': owner.id if owner else None,
            'product_id': product.id,
            'location_id': self.inventory.location_id.id,
        })


class TestConsignmentOwner(TestOwner):

    def _start_inventory_with_owner(self, owner):
        self.inventory.write({
            'consignment_supplier_id': owner.id,
            'filter': 'consignment',
        })
        self.inventory.action_start()

    def test_if_product_not_consignment__raise_error(self):
        self._start_inventory_with_owner(self.supplier_a)

        self.product_a.consignment = False
        self.inventory.line_ids = self._new_inventory_line(self.product_a, owner=self.supplier_a)

        with pytest.raises(ValidationError):
            self.inventory.action_validate()
