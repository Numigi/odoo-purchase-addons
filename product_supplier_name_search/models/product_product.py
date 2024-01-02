# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.addons.product_supplier_info_helpers.helpers import \
    get_products_from_supplier_info
from odoo.osv.expression import AND


class ProductProduct(models.Model):

    _inherit = "product.product"

    variant_supplier_ids = fields.One2many(
        "product.supplierinfo",
        "product_id",
        "Supplier Prices (Variant)",
    )

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        res = super().name_search(name=name, args=args, operator=operator, limit=limit)

        # The module only supports position operators.
        positive_operators = ["=", "ilike", "=ilike", "like", "=like"]
        if operator not in positive_operators:
            return res

        if limit is None or len(res) < limit:
            suppliers = _find_suppliers(self.env, operator, name)

            if suppliers:
                products = _find_products_from_suppliers(args, suppliers)
                res += products.name_get()

        res = _without_duplicates(res)
        return res[:limit]


def _find_suppliers(env, operator, name):
    return env["product.supplierinfo"].search(
        [
            "|",
            ("product_code", operator, name),
            ("product_name", operator, name),
        ]
    )


def _find_products_from_suppliers(args, suppliers):
    all_products = get_products_from_supplier_info(suppliers)
    domain = AND(
        (
            args or [],
            [("id", "in", all_products.ids)],
        )
    )
    product_cls = suppliers.env["product.product"]
    return product_cls.search(domain)


def _without_duplicates(res):
    return list(dict(res).items())
