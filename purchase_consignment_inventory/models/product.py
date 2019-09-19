# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons.purchase_consignment.models.common import get_products_from_supplier_info
from odoo.osv.expression import AND


class Product(models.Model):

    _inherit = 'product.product'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self._context.get('filter_products_by_consignment_supplier'):
            supplier_id = self._context['consignment_supplier_id']
            supplier_info = self.env['product.supplierinfo'].search([
                ('name.commercial_partner_id', '=', supplier_id),
            ])
            products = get_products_from_supplier_info(supplier_info)
            args = AND((args or [], [('id', 'in', products.ids)]))
        return super().name_search(name, args, operator, limit)
