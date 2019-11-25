# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase
from ..models.product import SUPPLIER_FILTER_CONTEXT_PARAM


class TestProduct(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_1 = cls.env['res.partner'].create({
            'name': 'My Partner Company 1',
            'supplier': True,
            'is_company': True,
        })
        cls.contact_1 = cls.env['res.partner'].create({
            'name': 'My Contact 1',
            'supplier': True,
            'is_company': False,
            'parent_id': cls.partner_1.id,
        })

        cls.partner_2 = cls.env['res.partner'].create({
            'name': 'My Partner Company 2',
            'supplier': True,
            'is_company': True,
        })

        cls.product_1 = cls.env['product.product'].create(cls._get_product_vals(cls.partner_1))
        cls.product_2 = cls.env['product.product'].create(cls._get_product_vals(cls.partner_2))

    @classmethod
    def _get_product_vals(cls, suppliers):
        return {
            'name': 'Test',
            'type': 'consu',
            'seller_ids': [
                (0, 0, {'name': p.id}) for p in suppliers
            ]
        }

    def _search_products(self, supplier):
        context = {
            SUPPLIER_FILTER_CONTEXT_PARAM: supplier.id if supplier else None,
        }
        return self.env['product.product'].with_context(**context).search([
            ('id', 'in', [self.product_1.id, self.product_2.id]),
        ])

    def test_search_product_with_no_supplier(self):
        assert not self._search_products(None)

    def test_search_product_with_commercial_partner(self):
        assert self._search_products(self.partner_1) == self.product_1
        assert self._search_products(self.partner_2) == self.product_2

    def test_search_product_with_contact(self):
        assert self._search_products(self.contact_1) == self.product_1
