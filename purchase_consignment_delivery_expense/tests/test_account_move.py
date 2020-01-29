# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class ExpenseOnDeliveryCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse = cls.env['stock.warehouse'].create({
            'name': 'W1',
            'code': 'W1',
        })

        cls.supplier = cls.env['res.partner'].create({
            'name': 'Supplier',
            'supplier': True,
        })

        cls.customer = cls.env['res.partner'].create({
            'name': 'Customer',
            'customer': True,
        })

        cls.expense_account = cls.env['account.account'].create({
            'name': 'Consignment Expense',
            'code': '555111',
            'user_type_id': cls.env.ref('account.data_account_type_expenses').id,
        })

        cls.transit_account = cls.env['account.account'].create({
            'name': 'Consignment Transit',
            'code': '222111',
            'user_type_id': cls.env.ref('account.data_account_type_current_liabilities').id,
        })

        cls.journal = cls.env['account.journal'].create({
            'name': 'Consignment Journal',
            'code': 'CJ',
            'type': 'general',
        })

        cls.category = cls.env['product.category'].create({
            'name': 'Consignment',
            'consignment': True,
            'consignment_delivery_expense': True,
            'property_cost_method': 'standard',
            'consignment_delivery_expense_account_id': cls.expense_account.id,
            'consignment_delivery_transit_account_id': cls.transit_account.id,
            'consignment_delivery_journal_id': cls.journal.id,
        })

        cls.cost = 50

        cls.product_uom = cls.env.ref('uom.product_uom_kgm')
        cls.product_po_uom = cls.env.ref('uom.product_uom_lb')

        cls.product = cls.env['product.product'].create({
            'name': 'Product A',
            'type': 'product',
            'categ_id': cls.category.id,
            'standard_price': cls.cost,
            'seller_ids': [(0, 0, {'name': cls.supplier.id})],
            'uom_id': cls.product_uom.id,
            'uom_po_id': cls.product_po_uom.id,
        })

        cls.quant = cls.env['stock.quant'].create({
            'product_id': cls.product.id,
            'quantity': 100,
            'owner_id': cls.supplier.id,
            'location_id': cls.warehouse.lot_stock_id.id,
        })

        cls.quantity = 10

        cls.order = cls.env['sale.order'].create({
            'partner_id': cls.customer.id,
            'warehouse_id': cls.warehouse.id,
            'order_line': [(0, 0, {
                'product_id': cls.product.id,
                'product_uom': cls.product_uom.id,
                'name': cls.product.name,
                'product_uom_qty': cls.quantity,
                'price_unit': 200,
                'date_planned': datetime.now(),
            })]
        })
        cls.order.action_confirm()
        cls.picking = cls.order.picking_ids
        cls.move = cls.picking.move_lines

    @classmethod
    def _process_picking(cls, picking):
        for line in picking.move_line_ids:
            line.qty_done = line.product_uom_qty
        picking.action_done()


class TestDelivery(ExpenseOnDeliveryCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._process_picking(cls.picking)
        cls.account_move = cls.move.account_move_ids
        cls.debit_line = cls.account_move.line_ids.filtered(lambda l: l.debit)
        cls.credit_line = cls.account_move.line_ids.filtered(lambda l: l.credit)

    def test_ref(self):
        assert self.account_move.ref == self.picking.name
        assert self.debit_line.ref == self.picking.name
        assert self.credit_line.ref == self.picking.name

    def test_move_line_name(self):
        assert self.debit_line.name == self.move.name
        assert self.credit_line.name == self.move.name

    def test_journal(self):
        assert self.account_move.journal_id == self.journal

    def test_cost(self):
        assert self.credit_line.credit == self.cost
        assert self.debit_line.debit == self.cost

    def test_product(self):
        assert self.credit_line.product_id == self.product
        assert self.debit_line.product_id == self.product

    def test_product_uom(self):
        assert self.credit_line.product_uom_id == self.product_uom
        assert self.debit_line.product_uom_id == self.product_uom

    def test_quantity(self):
        assert self.credit_line.quantity == self.quantity
        assert self.debit_line.quantity == self.quantity

    def test_account(self):
        assert self.debit_line.account_id == self.expense_account
        assert self.credit_line.account_id == self.transit_account

    def test_partner(self):
        assert self.debit_line.partner_id == self.supplier
        assert self.credit_line.partner_id == self.supplier


class TestDeliveryReturn(TestDelivery):
    """Test the return of a delivery of consigned products.

    On a delivery return, the debit and credit accounts are reversed.
    Otherwise, the journal entry is identical.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.picking = cls._return_picking(cls.picking)
        cls.move = cls.picking.move_lines
        cls.account_move = cls.move.account_move_ids
        cls.debit_line = cls.account_move.line_ids.filtered(lambda l: l.debit)
        cls.credit_line = cls.account_move.line_ids.filtered(lambda l: l.credit)

    @classmethod
    def _return_picking(cls, picking):
        wizard_obj = cls.env['stock.return.picking'].with_context(
            active_ids=[picking.id],
            active_id=picking.id,
        )
        wizard = wizard_obj.create(wizard_obj.default_get(list(wizard_obj._fields)))
        picking_id, dummy = wizard._create_returns()
        return_picking = cls.env['stock.picking'].browse(picking_id)
        cls._process_picking(return_picking)
        return return_picking

    def test_account(self):
        assert self.debit_line.account_id == self.transit_account
        assert self.credit_line.account_id == self.expense_account
