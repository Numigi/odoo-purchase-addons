# © 2018 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields
from odoo.addons.purchase.models.purchase import PurchaseOrder


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    block_auto_purchase_order = fields.Boolean(
        string="Block Automatic Product Add",
        default=False,
        states=PurchaseOrder.READONLY_STATES,
        help="When checked, this field prevents products from being automatically added "
        "to the PO by the system.",
    )
