# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import float_compare


def get_move_qty_in_po_line_uom(move: 'stock.move', po_line: 'purchase.order.line'):
    """Get the qty of a stock.move in the uom of the purchase order line.

    If the orderered qty is 10 kg and the received qty is 22.05 lbs,
    then, the full po line was received.

    In such case, we take 10 kg as the value to invoice.

    We do not convert the 22.05 lbs back in kilograms, because this would
    give 10.002 kg because of the rounding precision error.

    In case of a partial receipt, the quantity must be converted from the
    inventory uom to the purchase uom.

    The precision taken to compare the quantities is the inventory precision
    minus one. The reason is the core of Odoo contains multiple minor errors
    in rounding operations. Therefore, 10.002 should be the same as 10.000
    """
    moved_qty = move.product_uom._compute_quantity(
        move.product_uom_qty, po_line.product_uom,
        rounding_method='HALF-UP',
    )

    precision = move.env['decimal.precision'].precision_get('Product Unit of Measure') - 1
    is_full_qty = float_compare(
        moved_qty, po_line.product_qty, precision_digits=precision) == 0

    return po_line.product_qty if is_full_qty else moved_qty


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    receipt_picking_id = fields.Many2one(
        'stock.picking',
        string='Add Receipts',
        readonly=True, states={'draft': [('readonly', False)]},
        help='Load the vendor bill based on selected receipt. Several receipts can be selected.'
    )

    def _prepare_supplier_invoice_line_from_stock_move(self, move):
        po_line = move.purchase_line_id
        vals = self._prepare_invoice_line_from_po_line(po_line)

        quantity = get_move_qty_in_po_line_uom(move, po_line)

        if (
            (move.location_dest_id.usage == 'supplier' and self.type == 'in_invoice') or
            (move.location_dest_id.usage != 'supplier' and self.type == 'in_refund')
        ):
            quantity *= -1

        vals['quantity'] = quantity
        vals['receipt_move_id'] = move.id

        new_line = self.env['account.invoice.line'].new(vals)

        self.invoice_line_ids += new_line
        return new_line

    def _prepare_supplier_invoice_lines_from_receipt(self):
        for move in self.receipt_picking_id.move_lines:
            self._prepare_supplier_invoice_line_from_stock_move(move)

    @api.onchange('receipt_picking_id')
    def onchange_receipt_picking_id(self):
        if self.receipt_picking_id:
            self._prepare_supplier_invoice_lines_from_receipt()
            self.receipt_picking_id = False

    @api.onchange('invoice_line_ids')
    def _onchange_origin(self):
        """Override the default behavior for filling the invoice origin.

        The vanilla Odoo behavior is to find the PO related to each invoice line.

        The new behavior is based on the related receipt picking with a fallback on the related
        purchase order line.
        """
        lines_with_moves = self.invoice_line_ids.filtered(lambda l: l.receipt_move_id)
        lines_without_moves = self.invoice_line_ids - lines_with_moves

        receipts = lines_with_moves.mapped('receipt_move_id.picking_id')
        purchase_orders = lines_without_moves.mapped('purchase_id')

        if receipts or purchase_orders:
            references = (
                receipts.with_context(show_picking_supplier_reference=True).mapped('display_name') +
                purchase_orders.mapped('name')
            )
            self.origin = ', '.join(sorted(references))


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    receipt_move_id = fields.Many2one(
        'stock.move',
        string='Related Receipt Move',
        help='The stock move that generated this invoice line.'
    )

    receipt_picking_id = fields.Many2one(
        'stock.picking',
        related='receipt_move_id.picking_id',
        string='Receipt',
    )
