# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestVendorListConstraint(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env['res.partner'].create({
            'name': 'Supplier',
            'supplier': True,
        })

        cls.product = cls.env['product.product'].create({
            'name': 'Product A',
            'type': 'product',
            'consignment': True,
            'seller_ids': [(0, 0, {'name': cls.supplier.id})],
        })

    def test_if_consigned__can_not_have_more_than_one_supplier(self):
        new_supplier = self.supplier.copy()
        with pytest.raises(ValidationError):
            self.product.write({'seller_ids': [(0, 0, {'name': new_supplier.id})]})

    def test_two_price_entries_can_share_same_commercial_partner(self):
        new_contact = self.supplier.copy({'parent_id': self.supplier.id})
        self.product.write({'seller_ids': [(0, 0, {'name': new_contact.id})]})
        assert len(self.product.seller_ids) == 2
