# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.osv.expression import AND
from .common import get_products_from_supplier_id


class Product(models.Model):

    _inherit = "product.product"

    def _search(self, args, *args_, **kwargs):
        args = _add_supplier_domain_if_required(args, self.env, self._context)
        return super()._search(args, *args_, **kwargs)


def _add_supplier_domain_if_required(domain, env, context):
    partner_id = context.get("stock_inventory_partner_filter")
    if partner_id:
        products = get_products_from_supplier_id(env, partner_id)
        domain = AND((domain or [], [("id", "=", products.ids)]))
    return domain
