# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.osv.expression import AND
from odoo.addons.product_supplier_info_helpers.helpers import get_products_from_supplier_info

SUPPLIER_FILTER_CONTEXT_PARAM = 'filter_products_by_supplier'
SUPPLIER_FILTER_DISABLE_CONTEXT_PARAM = 'filter_products_by_supplier__disabled'


def _should_apply_supplier_filter(context: dict) -> bool:
    return (
        SUPPLIER_FILTER_CONTEXT_PARAM in context and
        not context.get(SUPPLIER_FILTER_DISABLE_CONTEXT_PARAM)
    )


def _get_products_from_supplier(supplier: 'res.partner') -> 'product.product':
    supplier_info = supplier.env['product.supplierinfo'].search([
        ('name.commercial_partner_id', '=', supplier.commercial_partner_id.id),
    ])
    return get_products_from_supplier_info(supplier_info)


def _get_domain_with_supplier_filter(env: 'Environment', domain: list) -> list:
    supplier_id = env.context[SUPPLIER_FILTER_CONTEXT_PARAM]

    if supplier_id:
        supplier = env['res.partner'].with_context(**{
            SUPPLIER_FILTER_DISABLE_CONTEXT_PARAM: True
        }).browse(supplier_id)
        products = _get_products_from_supplier(supplier)
        return AND((domain, [('id', 'in', products.ids)]))
    else:
        return [('id', '=', False)]


class Product(models.Model):

    _inherit = 'product.product'

    @api.model
    def _search(self, args, *args_, **kwargs):
        """Allow to filter products by a supplier given in context.

        If no supplier is selected on the PO, no product is shown.
        If a supplier is selected, only the products for this PO are shown.
        """
        if _should_apply_supplier_filter(self._context):
            args = _get_domain_with_supplier_filter(self.env, args or [])
        return super()._search(args, *args_, **kwargs)
