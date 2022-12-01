# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import StockInventoryCase


class TestProductSearchFilters(StockInventoryCase):

    def test_filter_partner(self):
        products = self._search_products({'stock_inventory_partner_filter': self.supplier_a.id})
        assert products == self.product_a

    def _search_products(self, context):
        return self.env['product.product'].with_context(**context).search([])
