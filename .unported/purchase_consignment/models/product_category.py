# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCategory(models.Model):

    _inherit = 'product.category'

    consignment = fields.Boolean(
        help="If checked, only one supplier can be selected in the supplier prices list "
        "for products of this category. "
        "The supplier will automatically be set as owner of the stock "
        "on receipt orders."
    )
