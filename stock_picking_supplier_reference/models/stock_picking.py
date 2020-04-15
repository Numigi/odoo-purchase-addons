# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv.expression import AND


class StockPicking(models.Model):

    _inherit = "stock.picking"

    supplier_reference = fields.Char(
        copy=False, index=True, track_visibility="onchange"
    )

    show_supplier_reference = fields.Boolean(compute="_compute_show_supplier_reference")

    @api.depends("location_id")
    def _compute_show_supplier_reference(self):
        for picking in self:
            picking.show_supplier_reference = picking.location_id.usage == "supplier"

    def name_get(self):
        """Show the supplier reference in the name of the picking.

        The context variable is used to have a specific format for picking names when
        selecting a picking for a supplier invoice.
        """
        if self._context.get("show_picking_supplier_reference"):
            return [(p.id, _get_formatted_picking_name(p)) for p in self]
        else:
            return super().name_get()

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        res = super().name_search(name, args, operator, limit)

        # The module only supports positive operators.
        positive_operators = ["=", "ilike", "=ilike", "like", "=like"]
        if operator not in positive_operators:
            return res

        if name and limit is None or len(res) < limit:
            ids_already_found = [r[0] for r in res]
            remaining_limit = None if limit is None else limit - len(res)

            domain = AND(
                (
                    (args or []),
                    [
                        "&",
                        ("id", "not in", ids_already_found),
                        "|",
                        ("supplier_reference", operator, name),
                        ("origin", operator, name),
                    ],
                )
            )

            pickings_with_supplier_reference = self.search(
                domain, limit=remaining_limit
            )

            res += pickings_with_supplier_reference.name_get()

        return res


def _get_formatted_picking_name(picking):
    name = picking.name

    if picking.supplier_reference:
        name = "{} - {}".format(name, picking.supplier_reference)

    if picking.origin:
        name = "{} ({})".format(name, picking.origin)

    return name
