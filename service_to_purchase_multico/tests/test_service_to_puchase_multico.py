# -*- coding: utf-8 -*-
# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.test_mail.tests.common import mail_new_test_user
from odoo.tests.common import TransactionCase


class TestServiceToPurchaseMultiCo(TransactionCase):
    def setUp(self):
        super(TestServiceToPurchaseMultiCo, self).setUp()

        self.company_1 = self.env["res.company"].create(
            {
                "name": "Test company 1",
            }
        )
        self.company_2 = self.env["res.company"].create(
            {
                "name": "Test company 2",
            }
        )
        self.user_1 = mail_new_test_user(
            self.env, login="user_1", groups="sales_team.group_sale_manager"
        )

        self.user_2 = mail_new_test_user(
            self.env, login="user_2", groups="sales_team.group_sale_manager"
        )

        self.user_1.write(
            {
                "company_id": self.company_1.id,
                "company_ids": [(6, 0, [self.company_1.id])],
            }
        )
        self.user_2.write(
            {
                "company_id": self.company_2.id,
                "company_ids": [(6, 0, [self.company_2.id])],
            }
        )

        self.service_purchase_1 = (
            self.env["product.product"]
            .sudo(self.user_1.id)
            .create(
                {
                    "name": "Service 1",
                    "standard_price": 200.0,
                    "list_price": 180.0,
                    "type": "service",
                    "service_to_purchase": True,
                }
            )
        )

    def test_service_to_purchase_company2(self):
        self.assertFalse(
            self.service_purchase_1.sudo(self.user_2.id).service_to_purchase
        )

    def test_service_to_purchase_company1(self):
        self.assertTrue(
            self.service_purchase_1.sudo(self.user_1.id).service_to_purchase
        )
