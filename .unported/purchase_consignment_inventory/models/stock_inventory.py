# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from itertools import groupby
from odoo import api, fields, models, _
from odoo.addons.product_supplier_info_helpers.helpers import (
    get_products_from_supplier_info,
)

CONSIGNMENT = "consignment"


class StockInventory(models.Model):

    _inherit = "stock.inventory"

    consignment_supplier_id = fields.Many2one(
        "res.partner", "Consignment Supplier", ondelete="restrict"
    )

    @api.onchange("filter")
    def _onchange_filter__if_consignment__set_exhausted(self):
        if self.filter == CONSIGNMENT:
            self.exhausted = True

    @api.onchange("filter")
    def _onchange_filter__if_not_consignment__unselect_supplier(self):
        if self.filter != CONSIGNMENT:
            self.consignment_supplier_id = None

    @api.model
    def _selection_filter(self):
        selection = super()._selection_filter()
        selection.append((CONSIGNMENT, _("Consignment Supplier")))
        return selection

    def _get_inventory_lines_values(self):
        if self.filter == CONSIGNMENT:
            return self._get_consignment_inventory_lines_values()
        else:
            return super()._get_inventory_lines_values()

    def _get_consignment_inventory_lines_values(self):
        all_products = self._get_all_products_for_consignment_supplier()
        quants = self._get_all_quants_in_inventoried_location(all_products)
        result = self._get_line_values_from_quants(quants)

        if self.exhausted:
            products_not_exhausted = quants.mapped("product_id")
            exhausted_products = all_products - products_not_exhausted
            result.extend(
                self._get_exhausted_consignment_line_values(exhausted_products)
            )

        return result

    def _get_all_products_for_consignment_supplier(self):
        supplier_info = self.env["product.supplierinfo"].search(
            [("name.commercial_partner_id", "=", self.consignment_supplier_id.id)]
        )
        all_products = get_products_from_supplier_info(supplier_info)
        return all_products.filtered(lambda p: p.consignment)

    def _get_all_quants_in_inventoried_location(self, products):
        locations = self.env["stock.location"].search(
            [("id", "child_of", [self.location_id.id])]
        )
        return self.env["stock.quant"].search(
            [("product_id", "in", products.ids), ("location_id", "in", locations.ids)]
        )

    def _get_line_values_from_quants(self, quants):
        result = []

        for dummy, quant_group in groupby(quants, _quant_group_by_key):
            quant_list = list(quant_group)
            quantity = sum(q.quantity for q in quant_list)
            first_quant = quant_list[0]
            result.append(
                {
                    "theoretical_qty": quantity,
                    "product_qty": quantity,
                    "product_uom_id": first_quant.product_id.uom_id.id,
                    "product_id": first_quant.product_id.id,
                    "location_id": first_quant.location_id.id,
                    "package_id": first_quant.package_id.id,
                    "prod_lot_id": first_quant.lot_id.id,
                    "partner_id": first_quant.owner_id.id,
                }
            )

        return result

    def _get_exhausted_consignment_line_values(self, products):
        return [
            {
                "theoretical_qty": 0,
                "product_qty": 0,
                "product_uom_id": p.uom_id.id,
                "product_id": p.id,
                "location_id": self.location_id.id,
                "package_id": None,
                "prod_lot_id": None,
                "partner_id": self.consignment_supplier_id.id,
            }
            for p in products
        ]


def _quant_group_by_key(quant):
    return (
        quant.product_id.id,
        quant.location_id.id,
        quant.lot_id.id,
        quant.package_id.id,
        quant.owner_id.id,
    )
