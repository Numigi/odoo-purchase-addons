# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestProductCategory(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env['product.category'].create({
            'name': 'Consignment',
            'consignment': True,
            'consignment_delivery_expense': True,
            'property_cost_method': 'standard',
        })

    def test_if_enabled__real_time_valuation_not_allowed(self):
        with pytest.raises(ValidationError):
            self.category.property_valuation = 'real_time'

    def test_if_enabled__periodic_valuation_allowed(self):
        self.category.property_valuation = 'manual_periodic'

    def test_if_disabled__real_time_valuation_allowed(self):
        self.category.consignment_delivery_expense = False
        self.category.property_valuation = 'real_time'

    def test_if_enabled__fifo_not_allowed(self):
        with pytest.raises(ValidationError):
            self.category.property_cost_method = 'fifo'

    def test_if_enabled__average_cost_not_allowed(self):
        with pytest.raises(ValidationError):
            self.category.property_cost_method = 'average'

    def test_if_enabled__standard_cost_allowed(self):
        self.category.property_cost_method = 'standard'

    def test_if_disabled__fifo_allowed(self):
        self.category.consignment_delivery_expense = False
        self.category.property_cost_method = 'fifo'

    def test_if_disabled__average_cost_allowed(self):
        self.category.consignment_delivery_expense = False
        self.category.property_cost_method = 'average'

    def test_if_consignment_disabled__delivery_expense_not_allowed(self):
        with pytest.raises(ValidationError):
            self.category.consignment = False
