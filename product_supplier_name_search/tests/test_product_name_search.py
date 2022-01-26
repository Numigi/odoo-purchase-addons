# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import data, ddt
from odoo.tests import common


@ddt
class TestProductNameSearch(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env["res.partner"].create(
            {"name": "Supplier", "supplier": True}
        )

        cls.table = cls.env["product.product"].create(
            {
                "name": "Wood Table",
                "type": "consu",
                "default_code": "WT2001",
                "seller_ids": [
                    (
                        0,
                        0,
                        {
                            "name": cls.supplier.id,
                            "product_name": "Brown Table",
                            "product_code": "BT1001",
                        },
                    )
                ],
            }
        )

        cls.chair = cls.env["product.product"].create(
            {
                "name": "Wood Chair",
                "type": "consu",
                "default_code": "WC2001",
                "seller_ids": [
                    (
                        0,
                        0,
                        {
                            "name": cls.supplier.id,
                            "product_name": "Brown Chair",
                            "product_code": "BC1001",
                        },
                    )
                ],
            }
        )

    def _search(self, name, operator="ilike", domain=None):
        items = self.env["product.product"].name_search(
            name, args=domain, operator=operator, limit=999999
        )
        return self.env["product.product"].browse([el[0] for el in items])

    def test_search_by_product_name(self):
        res = self._search("Wood")
        assert self.table in res
        assert self.chair in res

        res = self._search("Wood Table")
        assert self.table in res
        assert self.chair not in res

        res = self._search("Wood Chair")
        assert self.table not in res
        assert self.chair in res

    def test_search_by_product_default_code(self):
        res = self._search("2001")
        assert self.table in res
        assert self.chair in res

        res = self._search("WT2001")
        assert self.table in res
        assert self.chair not in res

        res = self._search("WC2001")
        assert self.table not in res
        assert self.chair in res

    def test_search_by_supplier_product_name(self):
        res = self._search("Brown")
        assert self.table in res
        assert self.chair in res

        res = self._search("Brown Table")
        assert self.table in res
        assert self.chair not in res

        res = self._search("Brown Chair")
        assert self.table not in res
        assert self.chair in res

    def test_search_by_supplier_product_code(self):
        res = self._search("1001")
        assert self.table in res
        assert self.chair in res

        res = self._search("BT1001")
        assert self.table in res
        assert self.chair not in res

        res = self._search("BC1001")
        assert self.table not in res
        assert self.chair in res

    def test_search_with_domain(self):
        res = self._search("1001", domain=[("id", "=", self.table.id)])
        assert self.table in res
        assert self.chair not in res

    def test_name_search_with_negative_operator(self):
        """Test that the module does not break the standard behavior of negative operators.

        The module only supports positive operators (i.e. `ilike`).
        If a negative operator is given, the supplier info will not be checked.
        """
        items = self._search("WT2001", operator="!=")
        assert self.table not in items
        assert self.chair in items

    @data("Wood", "Brown", "Table", "WT2001", "BT1001")
    def test_name_search_callable_with_none_limit(self, query):
        items = self.env["product.product"].name_search(
            query, operator="like", limit=None
        )
        products = self.env["product.product"].browse([el[0] for el in items])
        assert self.table in products
