# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo.tests.common import SavepointCase
from uuid import uuid4


class InvoiceFromPickingCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env['res.partner'].create({
            'name': 'Supplier',
            'supplier': True,
        })

        cls.po_uom = cls.env.ref('uom.product_uom_kgm')
        cls.stock_uom = cls.env.ref('uom.product_uom_lb')

        cls.product_a = cls.env['product.product'].create({
            'name': 'Product A',
            'type': 'product',
            'uom_id': cls.stock_uom.id,
            'uom_po_id': cls.po_uom.id,
        })

        cls.product_b = cls.env['product.product'].create({
            'name': 'Product B',
            'type': 'product',
            'uom_id': cls.stock_uom.id,
            'uom_po_id': cls.po_uom.id,
        })

        cls.qty_a = 10
        cls.qty_b = 20

        cls.order = cls.env['purchase.order'].create({
            'partner_id': cls.supplier.id,
            'order_line': [
                (0, 0, {
                    'product_id': cls.product_a.id,
                    'product_uom': cls.product_a.uom_po_id.id,
                    'name': cls.product_a.name,
                    'product_qty': cls.qty_a,
                    'price_unit': 100,
                    'date_planned': datetime.now(),
                }),
                (0, 0, {
                    'product_id': cls.product_b.id,
                    'product_uom': cls.product_b.uom_po_id.id,
                    'name': cls.product_b.name,
                    'product_qty': cls.qty_b,
                    'price_unit': 100,
                    'date_planned': datetime.now(),
                }),
            ]
        })
        cls.order.button_confirm()
        cls.picking = cls.order.picking_ids

        cls.invoice = cls.env['account.invoice'].create({
            'type': 'in_invoice',
            'partner_id': cls.supplier.id,
        })

    @staticmethod
    def _process_picking_entirely(picking):
        for move_line in picking.mapped('move_lines.move_line_ids'):
            move_line.qty_done = move_line.product_uom_qty
        picking.action_done()

    def _return_picking(self, picking):
        wizard_obj = self.env['stock.return.picking'].with_context(
            active_ids=[picking.id],
            active_id=picking.id,
        )
        wizard = wizard_obj.create(wizard_obj.default_get(list(wizard_obj._fields)))
        picking_id, dummy = wizard._create_returns()
        return_picking = self.env['stock.picking'].browse(picking_id)
        self._process_picking_entirely(return_picking)
        return return_picking


class TestInvoiceFromFullReceipt(InvoiceFromPickingCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._process_picking_entirely(cls.picking)

    def test_after_select_picking__one_line_created_per_stock_move(self):
        self.invoice.receipt_picking_id = self.picking
        self.invoice.onchange_receipt_picking_id()
        lines = self.invoice.invoice_line_ids
        assert len(lines) == 2
        assert lines[0].product_id == self.product_a
        assert lines[1].product_id == self.product_b

    def test_if_picking_is_receipt__quantity_is_positive(self):
        self.invoice.receipt_picking_id = self.picking
        self.invoice.onchange_receipt_picking_id()
        lines = self.invoice.invoice_line_ids
        assert len(lines) == 2
        assert lines[0].quantity == self.qty_a
        assert lines[1].quantity == self.qty_b

    def test_if_picking_is_return__quantity_is_negative(self):
        picking = self._return_picking(self.picking)
        self.invoice.receipt_picking_id = picking
        self.invoice.onchange_receipt_picking_id()
        lines = self.invoice.invoice_line_ids
        assert len(lines) == 2
        assert lines[0].quantity == -self.qty_a
        assert lines[1].quantity == -self.qty_b

    def test_if_picking_is_receipt__invoice_lines_bound_to_po_line(self):
        self.invoice.receipt_picking_id = self.picking
        self.invoice.onchange_receipt_picking_id()
        lines = self.invoice.invoice_line_ids
        assert len(lines) == 2
        assert lines[0].purchase_line_id == self.order.order_line[0]
        assert lines[1].purchase_line_id == self.order.order_line[1]

    def test_if_picking_is_return__invoice_lines_bound_to_po_line(self):
        picking = self._return_picking(self.picking)
        self.invoice.receipt_picking_id = picking
        self.invoice.onchange_receipt_picking_id()
        lines = self.invoice.invoice_line_ids
        assert len(lines) == 2
        assert lines[0].purchase_line_id == self.order.order_line[0]
        assert lines[1].purchase_line_id == self.order.order_line[1]

    def test_supplier_reference_added_to_invoice_origin(self):
        supplier_reference = str(uuid4())
        self.picking.supplier_reference = supplier_reference

        self.invoice.receipt_picking_id = self.picking
        self.invoice.onchange_receipt_picking_id()
        self.invoice._onchange_origin()

        assert supplier_reference in self.invoice.origin

    def test_invoice_filled_by_selecting_po__po_name_set_in_origin(self):
        self.invoice.purchase_id = self.order
        self.invoice.purchase_order_change()
        self.invoice._onchange_origin()

        assert self.order.name in self.invoice.origin


class TestInvoiceFromPartialReceipt(InvoiceFromPickingCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.received_qty_a = 5
        cls.received_qty_b = 10

        cls.expected_qty_a = 2.268  # 5 lbs -> 2.268 kg
        cls.expected_qty_b = 4.536  # 10 lbs -> 4.536 kg

        move_lines = cls.picking.mapped('move_lines.move_line_ids')
        move_line_a = move_lines.filtered(lambda l: l.product_id == cls.product_a)
        move_line_b = move_lines.filtered(lambda l: l.product_id == cls.product_b)
        move_line_a.qty_done = cls.received_qty_a
        move_line_b.qty_done = cls.received_qty_b

        cls.picking.action_done()

    def test_if_picking_is_receipt__quantity_is_positive(self):
        self.invoice.receipt_picking_id = self.picking
        self.invoice.onchange_receipt_picking_id()
        lines = self.invoice.invoice_line_ids
        assert len(lines) == 2
        assert lines[0].quantity == self.expected_qty_a
        assert lines[1].quantity == self.expected_qty_b

    def test_if_picking_is_return__quantity_is_negative(self):
        picking = self._return_picking(self.picking)
        self.invoice.receipt_picking_id = picking
        self.invoice.onchange_receipt_picking_id()
        lines = self.invoice.invoice_line_ids
        assert len(lines) == 2
        assert lines[0].quantity == -self.expected_qty_a
        assert lines[1].quantity == -self.expected_qty_b
