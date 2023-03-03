# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
import time


class TestPurchaseSaleInterCompanyDescriptionLine(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """
            ----------------------
            USERS AND THEIR GROUPS
            ----------------------
        """
        # Define groups
        grp_account_manager_id = cls.env.ref("account.group_account_manager").id
        grp_partner_manager_id = cls.env.ref("base.group_partner_manager").id
        grp_sale_manager_id = cls.env.ref("sales_team.group_sale_manager").id
        grp_purchase_manager_id = cls.env.ref("purchase.group_purchase_manager").id
        grp_system_id = cls.env.ref("base.group_system").id
        grp_multi_company_id = cls.env.ref("base.group_multi_company").id

        # Creating users A and B and their groups
        cls.user_a = cls.env["res.users"].create(
            {
                "name": "User company A",
                "login": "user_company_a",
                "email": "usercompany_a@testmail.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            grp_account_manager_id,
                            grp_partner_manager_id,
                            grp_sale_manager_id,
                            grp_purchase_manager_id,
                            grp_system_id,
                            grp_multi_company_id,
                        ],
                    )
                ],
            }
        )
        cls.user_b = cls.env["res.users"].create(
            {
                "name": "User company B",
                "login": "user_company_b",
                "email": "usercompany_b@testmail.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            grp_account_manager_id,
                            grp_partner_manager_id,
                            grp_sale_manager_id,
                            grp_purchase_manager_id,
                            grp_system_id,
                            grp_multi_company_id,
                        ],
                    )
                ],
            }
        )

        """
            ------------------------------------
            STOCK PARAMETERS FOR COMPANY A AND B
            ------------------------------------
        """
        # Stock location for warehouse for company B
        cls.location_stock_company_b = cls.env["stock.location"].create(
            {"name": "Stock - B", "usage": "internal"}
        )

        cls.location_output_company_b = cls.env["stock.location"].create(
            {"name": "Output - B", "usage": "internal"}
        )

        # Warehouse for company B
        cls.warehouse_company_b = cls.env["stock.warehouse"].create(
            {
                "name": "purchase warehouse - B",
                "code": "CMPB",
                "wh_input_stock_loc_id": cls.location_stock_company_b,
                "lot_stock_id": cls.location_stock_company_b,
                "wh_output_stock_loc_id": cls.location_output_company_b,
            }
        )

        # Stock location for warehouse for company A
        cls.location_stock_company_a = cls.env["stock.location"].create(
            {"name": "Stock - A", "usage": "internal"}
        )

        cls.location_output_company_a = cls.env["stock.location"].create(
            {"name": "Output - A", "usage": "internal"}
        )

        # Warehouse for company A
        cls.warehouse_company_a = cls.env["stock.warehouse"].create(
            {
                "name": "purchase warehouse - A",
                "code": "CMPA",
                "wh_input_stock_loc_id": cls.location_stock_company_a,
                "lot_stock_id": cls.location_stock_company_a,
                "wh_output_stock_loc_id": cls.location_output_company_a,
            }
        )

        """
            -------------------------------------------
            COMPANY A/B AND INTER COMPANY CONFIGURATION
            -------------------------------------------
        """
        # Activating auto sale auto validation on company A
        cls.company_a = cls.env["res.company"].create(
            {
                "name": "Company-A",
                "warehouse_id": cls.warehouse_company_a.id,
                "sale_auto_validation": 1,
            }
        )

        # Activating auto sale auto validation on company B
        cls.company_b = cls.env["res.company"].create(
            {
                "name": "Company-B",
                "warehouse_id": cls.warehouse_company_b.id,
                "sale_auto_validation": 1,
            }
        )

        """
            -------------------------
            USERS COMPANY ASSIGNATION
            -------------------------
        """
        cls.user_a.refresh()
        cls.user_b.refresh()

        # Assign user A to company A and B
        cls.user_a.write(
            {
                "company_id": cls.company_a.id,
                "company_ids": [(6, 0, [cls.company_a.id, cls.company_b.id])],
            }
        )

        # Assign user B to company A and B
        cls.user_b.write(
            {
                "company_id": cls.company_b.id,
                "company_ids": [(6, 0, [cls.company_a.id, cls.company_b.id])],
            }
        )

        """
            -------------------------------------------
            COMPANY A/B INTER COMPANY CONFIGURATION AND
            AUTO GENERATION OF SO FROM PO PARAMETERS
            -------------------------------------------
        """
        cls.company_b.so_from_po = True
        cls.company_a.so_from_po = True

        cls.warehouse_company_b.refresh()
        cls.location_stock_company_b.refresh()
        cls.location_output_company_b.refresh()
        cls.location_stock_company_a.refresh()
        cls.location_output_company_a.refresh()

        cls.warehouse_company_a.company_id = cls.company_a.id
        cls.warehouse_company_b.company_id = cls.company_b.id
        cls.location_stock_company_b.company_id = cls.company_b.id
        cls.location_output_company_b.company_id = cls.company_b.id
        cls.location_stock_company_a.company_id = cls.company_a.id
        cls.location_output_company_a.company_id = cls.company_a.id

        # Getting sale and purchase manager
        cls.purchase_manager_gr = cls.env.ref("purchase.group_purchase_manager")
        cls.sale_manager_gr = cls.env.ref("sales_team.group_sale_manager")

        # Creating an intercompany user and link to each company
        cls.intercompany_user = cls.user_b.copy()
        cls.intercompany_user.company_ids |= cls.company_a
        cls.company_b.intercompany_user_id = cls.intercompany_user
        cls.company_a.intercompany_user_id = cls.intercompany_user

        """
            ---------------------------------
            ACCOUNT AND PRODUCT CONFIGURATION
            ---------------------------------
        """
        cls.account_sale_b = cls.env["account.account"].create(
            {
                "code": "BNK",
                "name": "Bank account (test)",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_liquidity").id,
            }
        )

        cls.product_consultant = cls.env["product.product"].create(
            {
                "name": "Service Multi Company",
                "uom_id": cls.env.ref("uom.product_uom_hour").id,
                "uom_po_id": cls.env.ref("uom.product_uom_hour").id,
                "type": "service",
                "company_id": False,
            }
        )

        cls.product_consultant.sudo(
            cls.user_b.id
        ).property_account_income_id = cls.account_sale_b
        currency_cad = cls.env.ref("base.CAD")

        # Settings for price policy
        pricelists = (
            cls.env["product.pricelist"]
            .sudo()
            .search([("currency_id", "!=", currency_cad.id)])
        )

        cls.company_b.intercompany_overwrite_purchase_price = True
        cls.company_a.intercompany_overwrite_purchase_price = True

        # Set all price list to CAD
        for pl in pricelists:
            pl.currency_id = currency_cad

        """
            -------------------------------------
            PURCHASE ORDER CREATED FROM COMPANY A
            -------------------------------------
        """
        cls.purchase_company_a = cls.env["purchase.order"].create(
            {
                "state": "draft",
                "partner_id": cls.user_b.partner_id.id,
                "company_id": cls.company_a.id,
            }
        )
        cls.purchase_line_company_a = cls.env["purchase.order.line"].create(
            {
                "order_id": cls.purchase_company_a.id,
                "product_id": cls.product_consultant.id,
                "product_uom": cls.env.ref("uom.product_uom_hour").id,
                "name": "Service Multi Company",
                "price_unit": 450.0,
                "product_qty": 3.0,
                "date_planned": time.strftime("%Y%m%d"),
                "product_qty": 3.0,
                "company_id": cls.company_a.id,
            }
        )

        cls.purchase_company_a.currency_id = currency_cad

    def test_purchase_sale_inter_company_description_line(self):
        self.user_b.partner_id.write({
            "ref_company_ids": [(6, 0, [self.company_a.id])]
            })
        
        # TODO: in_type_id value to check
        self.company_a.po_picking_type_id = self.warehouse_company_a.in_type_id.id
        
        # Approve PO to create the SO for company B
        self.purchase_company_a.sudo(self.user_a).button_approve()
        self.purchase_company_a.refresh()

        # TODO : Here we get empty result if we show
        # the return of button_approve()
        # Check _inter_company_create_sale_order()
        # and button_approve() function in purchase_order.py
        # of `purchase_sale_inter_company` module for further details

        # Make sure that user B belongs to company B
        self.user_b.company_id = self.company_b.id

        sales = (
            self.env["sale.order"]
            .sudo(self.user_b)
            .search([("auto_purchase_order_id", "=", self.purchase_company_a.id)])
        )

        # Checking the SO and its order line was created from PO
        self.assertNotEquals(sales, False)
        self.assertEquals(len(sales), 1)
        self.assertEquals(
            len(sales.order_line), len(self.purchase_company_a.order_line)
        )

        # Checking product/description from PO to SO
        # on order line that it was kept
        for index in range(len(sales.order_line)):
            self.assertEquals(
                sales.order_line[index].product_id,
                self.purchase_company_a.order_line[index].product_id,
            )
            self.assertEquals(
                sales.order_line[index].description,
                self.purchase_company_a.order_line[index].description,
            )
