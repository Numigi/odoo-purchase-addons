# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.addons.product_supplier_info_helpers.helpers import (
    get_supplier_info_from_product,
)


class StockMove(models.Model):

    _inherit = 'stock.move'

    def _action_done(self):
        moves = super()._action_done()

        moves_with_company_forced = (
            m.with_context(force_company=m.company_id.id) for m in moves
        )
        moves_that_require_expense_move = (
            m for m in moves_with_company_forced
            if m._requires_consginment_expense_account_move()
        )

        for move in moves_that_require_expense_move:
            move.sudo()._create_consignment_expense_account_move()

        return moves

    def _requires_consginment_expense_account_move(self):
        return self._is_consignment_delivery() or self._is_consignment_delivery_return()

    def _is_consignment_delivery(self):
        return (
            self.product_id.categ_id.consignment_delivery_expense and
            self.location_id.usage == 'internal' and
            self.location_dest_id.usage == 'customer'
        )

    def _is_consignment_delivery_return(self):
        return (
            self.product_id.categ_id.consignment_delivery_expense and
            self.location_id.usage == 'customer' and
            self.location_dest_id.usage == 'internal'
        )

    def _create_consignment_expense_account_move(self):
        vals = self._get_consignment_expense_account_move_vals()
        move = self.env['account.move'].create(vals)
        move.post()

    def _get_consignment_expense_account_move_vals(self):
        return {
            'date': fields.Date.context_today(self),
            'ref': self.picking_id.name,
            'journal_id': self.product_id.categ_id.consignment_delivery_journal_id.id,
            'stock_move_id': self.id,
            'line_ids': [
                (0, 0, self._get_consignment_expense_move_line_vals()),
                (0, 0, self._get_consignment_transit_move_line_vals()),
            ]
        }

    def _get_consignment_expense_move_line_vals(self):
        vals = self._get_common_consignment_account_move_line_vals()

        category = self.product_id.categ_id
        vals['account_id'] = category.consignment_delivery_expense_account_id.id

        cost = self._get_consignment_expense_cost()
        is_return = self._is_consignment_delivery_return()
        vals['debit'] = 0 if is_return else cost
        vals['credit'] = cost if is_return else 0

        return vals

    def _get_consignment_transit_move_line_vals(self):
        vals = self._get_common_consignment_account_move_line_vals()

        category = self.product_id.categ_id
        vals['account_id'] = category.consignment_delivery_transit_account_id.id

        cost = self._get_consignment_expense_cost()
        is_return = self._is_consignment_delivery_return()
        vals['debit'] = cost if is_return else 0
        vals['credit'] = 0 if is_return else cost

        return vals

    def _get_common_consignment_account_move_line_vals(self):
        return {
            'name': self.name,
            'product_id': self.product_id.id,
            'quantity': self.product_uom_qty,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': self.picking_id.name,
            'partner_id': self._get_consignment_expense_partner().id,
        }

    def _get_consignment_expense_cost(self):
        return self.product_id.standard_price

    def _get_consignment_expense_partner(self):
        owner = self.move_line_ids.mapped('owner_id')

        if not owner:
            supplier_info = get_supplier_info_from_product(self.product_id)
            owner = supplier_info.mapped('name.commercial_partner_id')

        return owner[0]
