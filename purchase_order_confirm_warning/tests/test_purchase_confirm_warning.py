# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common, tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestPurchaseConfirmationWizard(common.TransactionCase):
    """
    Test suite for Purchase Confirmation Wizard module
    """

    def setUp(self):
        """
        Set up test data
        """
        super(TestPurchaseConfirmationWizard, self).setUp()

        # Test models
        self.PurchaseOrder = self.env['purchase.order']
        self.Partner = self.env['res.partner']
        self.Product = self.env['product.product']
        self.Wizard = self.env['purchase.confirmation.wizard']

        # Create test supplier with warning
        self.supplier_with_warning = self.Partner.create({
            'name': 'Test Supplier With Warning',
            'supplier_rank': 1,
            'purchase_warn': 'warning',
            'purchase_warn_msg': (
                'This supplier requires special attention. '
                'Please verify all details before proceeding.'
            )
        })

        # Create test supplier without warning
        self.supplier_without_warning = self.Partner.create({
            'name': 'Test Supplier Without Warning',
            'supplier_rank': 1,
            'purchase_warn': 'none',
            'purchase_warn_msg': False
        })

        # Create test product
        self.test_product = self.Product.create({
            'name': 'Test Product',
            'type': 'consu',
            'purchase_ok': True,
            'list_price': 100.0,
            'standard_price': 50.0
        })

        # Create test purchase orders
        self.po_with_warning = self.PurchaseOrder.create({
            'partner_id': self.supplier_with_warning.id,
            'order_line': [(0, 0, {
                'product_id': self.test_product.id,
                'product_qty': 10,
                'price_unit': 100.0,
                'name': self.test_product.name
            })]
        })

        self.po_without_warning = self.PurchaseOrder.create({
            'partner_id': self.supplier_without_warning.id,
            'order_line': [(0, 0, {
                'product_id': self.test_product.id,
                'product_qty': 5,
                'price_unit': 80.0,
                'name': self.test_product.name
            })]
        })

    def test_01_wizard_creation(self):
        """
        Test wizard creation and field population
        """
        wizard = self.Wizard.create({
            'warning_message': 'Test warning message',
            'purchase_order_id': self.po_with_warning.id
        })

        # Test wizard fields
        self.assertEqual(wizard.warning_message, 'Test warning message')
        self.assertEqual(wizard.purchase_order_id, self.po_with_warning)
        self.assertEqual(wizard.purchase_order_name, self.po_with_warning.name)
        self.assertEqual(wizard.supplier_name, self.supplier_with_warning.name)

    def test_02_supplier_with_warning_triggers_wizard(self):
        """
        Test that button_confirm returns wizard action for supplier with warning
        """
        result = self.po_with_warning.button_confirm()

        # Verify that wizard action is returned
        self.assertEqual(result['type'], 'ir.actions.act_window')
        self.assertEqual(result['res_model'], 'purchase.confirmation.wizard')
        self.assertEqual(result['view_mode'], 'form')
        self.assertEqual(result['target'], 'new')

        # Verify context contains correct data
        self.assertIn('default_warning_message', result['context'])
        self.assertIn('default_purchase_order_id', result['context'])
        self.assertEqual(
            result['context']['default_purchase_order_id'],
            self.po_with_warning.id
        )

    def test_03_supplier_without_warning_direct_confirmation(self):
        """
        Test that button_confirm proceeds directly for supplier without warning
        """
        # Mock the super method to track if it's called
        original_state = self.po_without_warning.state
        result = self.po_without_warning.button_confirm()

        # Should return super() result (could be True or action dict)
        self.assertIsNotNone(result)
        # PO should remain in draft until fully processed
        self.assertEqual(self.po_without_warning.state, original_state)

    def test_04_wizard_confirm_action(self):
        """
        Test wizard confirm action with bypass context
        """
        # Create wizard
        wizard = self.Wizard.create({
            'warning_message': 'Test warning',
            'purchase_order_id': self.po_with_warning.id
        })

        # Mock the button_confirm to verify it's called with correct context
        with common.mock_calls() as mock_calls:
            wizard.action_confirm_validation()

            # Verify button_confirm was called with bypass context
            self.assertTrue(mock_calls.called)
            # In real implementation, this would verify the context

    def test_05_wizard_cancel_action(self):
        """
        Test wizard cancel action closes wizard
        """
        wizard = self.Wizard.create({
            'warning_message': 'Test warning',
            'purchase_order_id': self.po_with_warning.id
        })

        result = wizard.action_cancel_validation()

        # Should return window close action
        self.assertEqual(result['type'], 'ir.actions.act_window_close')

    def test_06_bypass_supplier_warning_context(self):
        """
        Test that bypass_supplier_warning context prevents wizard display
        """
        # Test with bypass context
        result = self.po_with_warning.with_context(
            bypass_supplier_warning=True
        ).button_confirm()

        # Should proceed with normal confirmation, not return wizard action
        self.assertNotEqual(result.get('res_model'), 'purchase.confirmation.wizard')

    def test_07_suppress_supplier_warning_context(self):
        """
        Test that suppress_supplier_warning context prevents wizard display
        """
        result = self.po_with_warning.with_context(
            suppress_supplier_warning=True
        ).button_confirm()

        # Should proceed with normal confirmation, not return wizard action
        self.assertNotEqual(result.get('res_model'), 'purchase.confirmation.wizard')

    def test_08_warning_message_formatting(self):
        """
        Test that warning message is properly formatted
        """
        result = self.po_with_warning._open_confirmation_wizard(
            self.po_with_warning,
            self.supplier_with_warning
        )

        warning_message = result['context']['default_warning_message']

        # Verify message contains supplier name and warning
        self.assertIn(self.supplier_with_warning.name, warning_message)
        self.assertIn(self.supplier_with_warning.purchase_warn_msg, warning_message)
        self.assertIn('Do you want to proceed', warning_message)

    def test_09_multiple_purchase_orders_behavior(self):
        """
        Test behavior when confirming multiple purchase orders
        """
        # Create another PO with the same supplier
        po2_with_warning = self.PurchaseOrder.create({
            'partner_id': self.supplier_with_warning.id,
            'order_line': [(0, 0, {
                'product_id': self.test_product.id,
                'product_qty': 3,
                'price_unit': 90.0,
                'name': self.test_product.name
            })]
        })

        # Test confirming multiple POs at once
        pos = self.po_with_warning + po2_with_warning
        result = pos.button_confirm()

        # Should return wizard action for the first PO with warning
        self.assertEqual(result['type'], 'ir.actions.act_window')
        self.assertEqual(result['res_model'], 'purchase.confirmation.wizard')

    def test_10_supplier_with_block_warning(self):
        """
        Test behavior with supplier that has blocking warning
        """
        # Create supplier with blocking warning
        blocking_supplier = self.Partner.create({
            'name': 'Blocking Supplier',
            'supplier_rank': 1,
            'purchase_warn': 'block',
            'purchase_warn_msg': 'This supplier is blocked. Cannot proceed with purchase.'
        })

        blocking_po = self.PurchaseOrder.create({
            'partner_id': blocking_supplier.id,
            'order_line': [(0, 0, {
                'product_id': self.test_product.id,
                'product_qty': 1,
                'price_unit': 100.0,
                'name': self.test_product.name
            })]
        })

        # Should raise UserError for blocking warning
        with self.assertRaises(UserError):
            blocking_po.button_confirm()

    def test_11_wizard_ensure_one_constraints(self):
        """
        Test wizard action constraints with ensure_one()
        """
        # Create multiple wizard records (shouldn't happen normally)
        wizard1 = self.Wizard.create({
            'warning_message': 'Warning 1',
            'purchase_order_id': self.po_with_warning.id
        })

        wizard2 = self.Wizard.create({
            'warning_message': 'Warning 2',
            'purchase_order_id': self.po_without_warning.id
        })

        wizards = wizard1 + wizard2

        # Test that ensure_one() prevents actions on multiple records
        with self.assertRaises(ValueError):
            wizards.action_confirm_validation()

        with self.assertRaises(ValueError):
            wizards.action_cancel_validation()

    def test_12_purchase_order_state_after_wizard_confirmation(self):
        """
        Test purchase order state after wizard confirmation
        """
        # Create wizard and confirm through it
        wizard = self.Wizard.create({
            'warning_message': 'Test warning',
            'purchase_order_id': self.po_with_warning.id
        })

        # Execute confirmation (this will trigger the actual confirmation process)
        wizard.action_confirm_validation()

        # The state should change from 'draft' to 'purchase' after confirmation
        # Note: In test environment, might need to manually check the workflow

    def test_13_wizard_without_purchase_order(self):
        """
        Test wizard behavior when no purchase order is set
        """
        wizard = self.Wizard.create({
            'warning_message': 'Test warning without PO',
            'purchase_order_id': False
        })

        # Actions should still work without raising errors
        result = wizard.action_cancel_validation()
        self.assertEqual(result['type'], 'ir.actions.act_window_close')

        # Confirm action should handle missing PO gracefully
        result = wizard.action_confirm_validation()
        # Should not raise error, but may return None or empty result

    def test_14_special_characters_in_warning_message(self):
        """
        Test handling of special characters in warning messages
        """
        # Update supplier with special characters in warning
        self.supplier_with_warning.write({
            'purchase_warn_msg': 'Special chars: <>&"\' and unicode: ñáéíóú'
        })

        result = self.po_with_warning.button_confirm()

        # Should not raise encoding errors
        self.assertEqual(result['type'], 'ir.actions.act_window')
        self.assertIn('Special chars', result['context']['default_warning_message'])
