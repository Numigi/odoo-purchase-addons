# -*- coding: utf-8 -*-
# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-v3).

from odoo.tests.common import TransactionCase

from datetime import datetime

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TestPurchaseOrder(TransactionCase):

    def setUp(self):
        super(TestPurchaseOrder, self).setUp()
        # Useful models
        self.PurchaseOrder = self.env['purchase.order']
        self.WizardAlert = self.env['wizard.alert']
        self.ResConfigSetting = self.env['res.config.settings']
        self.PurchaseOrderLine = self.env['purchase.order.line']
        self.partner_id = self.env.ref('base.res_partner_1')
        self.partner_id.write({'min_purchase_amount': 500})
        self.product_id_1 = self.env.ref('product.product_product_8')
        res_users_purchase_user = self.env.ref('purchase.group_purchase_user')

        self.po_1_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 6.0,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 100.0,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }

        self.po_2_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 4.0,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 100.0,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }

        self.po_3_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 7.0,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 100.0,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }

        self.po_4_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 4.0,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 100.0,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }

        users = self.env['res.users'].with_context({'no_reset_password': True, 'mail_create_nosubscribe': True})
        self.user_purchase_user = users.create({
            'name': 'Pauline Poivraisselle',
            'login': 'pauline',
            'email': 'pur@example.com',
            'notification_type': 'inbox',
            'groups_id': [(6, 0, [res_users_purchase_user.id])]})

    def test_confirm_po_without_alert_msg(self):
        # Create purchase with amount untaxed 600
        self.po_1 = self.PurchaseOrder.create(self.po_1_vals)
        self.assertTrue(self.po_1, 'Purchase: no purchase order created')
        self.assertEqual(self.po_1.amount_untaxed, 600.0)
        # Confirm Order
        # When confirm, the order must be confirmed (600 > minimum purchase amount : 500)
        res_confirm = self.po_1.button_confirm()
        self.assertTrue(res_confirm, 'Purchase: The purchase order has not confirmed')

    def test_confirm_po_with_alert_msg(self):
        # Create purchase with amount untaxed 400
        self.po_2 = self.PurchaseOrder.create(self.po_2_vals)
        self.assertTrue(self.po_2, 'Purchase: no purchase order created')
        self.assertEqual(self.po_2.amount_untaxed, 400.0)
        # Confirm Order
        # When confirm, the warning must be appear (400 < minimum purchase amount : 500)
        res_confirm = self.po_2.button_confirm()
        self.assertTrue(res_confirm['context']['to_confirm'],
                        'Purchase: PO The Minimum Purchase amount must be lower then amount untaxed of this purchase"')
        self.alerte_1 = self.WizardAlert.create({'order_id': self.po_2.id})
        res_confirm = self.alerte_1.with_context({'to_confirm': True}).apply()
        self.assertTrue(res_confirm, 'Purchase: The purchase order has not confirmed')

    def test_approve_po_without_alert_msg(self):

        self.env.user.company_id.write({'po_double_validation': 'two_step','po_double_validation_amount': 300.00})

        self.po_3 = self.PurchaseOrder.sudo(self.user_purchase_user).create(self.po_3_vals)
        self.assertTrue(self.po_3, 'Purchase: no purchase order created')
        self.assertEqual(self.po_3.amount_untaxed, 700.0)

        res_confirm = self.po_3.button_confirm()
        self.assertTrue(res_confirm, 'Purchase: The purchase order has not confirmed')
        self.assertEqual(self.po_3.state, 'to approve', 'Purchase: PO state should be "to approve".')


        self.po_3.button_approve()
        self.assertEqual(self.po_3.state, 'purchase', 'PO state should be "Purchase".')

    def test_approve_po_with_alert_msg(self):

        self.env.user.company_id.write({'po_double_validation': 'two_step', 'po_double_validation_amount': 300.00})

        self.po_4 = self.PurchaseOrder.sudo(self.user_purchase_user).create(self.po_4_vals)
        self.assertTrue(self.po_4, 'Purchase: no purchase order created')
        self.assertEqual(self.po_4.amount_untaxed, 400.0)

        res_confirm = self.po_4.button_confirm()
        self.assertTrue(res_confirm['context']['to_confirm'],
                        'Purchase: PO The Minimum Purchase amount must be lower then amount untaxed of this purchase"')

        self.alerte_2 = self.WizardAlert.create({'order_id': self.po_4.id})
        res_confirm = self.alerte_2.with_context({'to_confirm': True}).apply()
        self.assertTrue(res_confirm, 'Purchase: The purchase order has not confirmed')
        self.po_4.button_approve()
        self.assertEqual(self.po_4.state, 'purchase', 'Purchase: PO state should be "to Purchase".')
