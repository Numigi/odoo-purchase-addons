# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class StockInventoryCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._activate_owner_option_on_inventories()

        cls.supplier_a = cls.env["res.partner"].create(
            {"name": "Supplier", "supplier": True}
        )

        cls.supplier_a_contact = cls.env["res.partner"].create(
            {
                "name": "Contact A",
                "supplier": True,
                "is_company": False,
                "parent_id": cls.supplier_a.id,
            }
        )

        cls.category_1 = cls.env["product.category"].create(
            {"name": "Category 1", "consignment": True}
        )
        cls.product_a = cls.env["product.product"].create(
            {
                "name": "Product A",
                "categ_id": cls.category_1.id,
                "type": "product",
                "consignment": True,
                "seller_ids": [(0, 0, {"name": cls.supplier_a.id})],
            }
        )
        cls.product_b = cls.env["product.product"].create(
            {
                "name": "Product B",
                "categ_id": cls.category_1.id,
                "type": "product",
                "consignment": True,
            }
        )

        cls.inventory = cls.env["stock.inventory"].create({"name": "New Inventory"})

    @classmethod
    def _activate_owner_option_on_inventories(cls):
        cls.env.user.groups_id |= cls.env.ref("stock.group_tracking_owner")
