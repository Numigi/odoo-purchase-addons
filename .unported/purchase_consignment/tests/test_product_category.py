# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from ddt import ddt, data
from odoo.tests.common import SavepointCase


@ddt
class TestPropagationToProduct(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create({"name": "Product A"})
        cls.category = cls.env["product.category"].create(
            {"name": "Consignment", "consignment": True}
        )

    @data(True, False)
    def test_on_change_category__value_propagated_to_product(self, value):
        self.category.consignment = value
        self.product.categ_id = self.category
        assert self.product.consignment is value


class TestPropagationToProductTemplate(TestPropagationToProduct):
    """Behavior should be the same with product as with product template."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.product.product_tmpl_id
