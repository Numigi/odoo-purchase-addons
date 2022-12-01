# © 2018 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields
from .purchase_order import BLOCK_AUTO_HELP


class ProductTemplate(models.Model):

    _inherit = "product.template"

    block_auto_purchase_order = fields.Boolean(
        string="Block Automatic Product Add",
        help=BLOCK_AUTO_HELP,
    )
