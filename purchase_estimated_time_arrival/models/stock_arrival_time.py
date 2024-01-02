# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

SECONDS_PER_DAY = 86400  # 24 * 60 * 60


class StockArrivalTime(models.Model):

    _name = "stock.arrival.time"
    _description = "Stock Arrival Time"
    _order = "receipt_date desc"

    move_id = fields.Many2one(
        "stock.move",
        "Receipt Move",
        ondelete="restrict",
    )

    picking_id = fields.Many2one(
        "stock.picking",
        "Receipt",
        related="move_id.picking_id",
        store=True,
    )

    purchase_order_id = fields.Many2one(
        "purchase.order",
        "Purchase Order",
        related="move_id.purchase_line_id.order_id",
        store=True,
    )

    supplier_id = fields.Many2one(
        "res.partner",
        "Supplier",
        related="purchase_order_id.partner_id",
        store=True,
    )

    product_id = fields.Many2one(
        "product.product",
        "Product",
        required=True,
        index=True,
    )
    product_tmpl_id = fields.Many2one(
        "product.template",
        related="product_id.product_tmpl_id",
        store=True,
        index=True,
    )

    purchase_date = fields.Datetime(required=True)
    receipt_date = fields.Datetime(required=True, index=True)

    days = fields.Float(compute="_compute_days", store=True, group_operator="avg")

    @api.depends("purchase_date", "receipt_date")
    def _compute_days(self):
        for line in self:
            arrival_in_seconds = (
                line.receipt_date - line.purchase_date
            ).total_seconds()
            line.days = arrival_in_seconds / SECONDS_PER_DAY
