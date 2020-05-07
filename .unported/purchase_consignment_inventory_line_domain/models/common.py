# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.product_supplier_info_helpers.helpers import (
    get_products_from_supplier_info,
)


def get_products_from_supplier_id(env, partner_id):
    supplier_info = env["product.supplierinfo"].search(
        [
            "|",
            ("name", "=", partner_id),
            ("name.commercial_partner_id", "=", partner_id),
        ]
    )
    return get_products_from_supplier_info(supplier_info)
