# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from datetime import datetime

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError


class TestPurchaseOrder(TransactionCase):

    def setUp(self):
        super(TestPurchaseOrder, self).setUp()
        # Useful models
        self.PurchaseOrder = self.env['purchase.order']
        self.PurchaseOrderLine = self.env['purchase.order.line']
        self.ProductProduct = self.env['product.product']
        self.partner_id_1 = self.env.ref('base.res_partner_1')
        self.partner_id_2 = self.env.ref('base.res_partner_3')
        self.product_categ_id = self.env.ref('product.product_category_5')
        self.uom_unit = self.env.ref('uom.product_uom_unit')

        self.product_1_vals = {
            'name': 'Acier Lac 1.2',
            'categ_id': self.product_categ_id.id,
            'type': 'consu',
            'uom_id': self.uom_unit.id,
            'uom_po_id': self.uom_unit.id,
            'default_code': 'ACIERLC2',
            'seller_ids': [
            (0, 0, {
                'name': self.partner_id_1.id,
            })]
        }

        self.product_2_vals = {
            'name': 'Acier Lac 3.4',
            'categ_id': self.product_categ_id.id,
            'type': 'consu',
            'uom_id': self.uom_unit.id,
            'uom_po_id': self.uom_unit.id,
            'default_code': 'ACIERLC3',
            'seller_ids': [
                (0, 0, {
                    'name': self.partner_id_2.id,
                })]
        }
        # Create product
        self.product_id_1 = self.ProductProduct.create(self.product_1_vals)
        self.product_id_2 = self.ProductProduct.create(self.product_2_vals)

    def test_create_po_with_partner_in_list_seller_of_product(self):
        # Test create PO 1 with partner in list seller of product in line order
        self.po_1_vals = {
            'partner_id': self.partner_id_1.id,
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

        self.po_1 = self.PurchaseOrder.create(self.po_1_vals)
        self.assertTrue(self.po_1, 'Purchase: no purchase order created')

    def test_create_po_with_partner_not_in_list_seller_of_product(self):
        # Test create PO 2 with partner not in list seller of product in line order
        self.po_2_vals = {
            'partner_id': self.partner_id_1.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_2.name,
                    'product_id': self.product_id_2.id,
                    'product_qty': 6.0,
                    'product_uom': self.product_id_2.uom_po_id.id,
                    'price_unit': 100.0,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }

        with self.assertRaises(ValidationError):
            self.po_2 = self.PurchaseOrder.create(self.po_2_vals)

    def test_edit_po_with_partner_not_in_list_seller_of_product(self):
        # Test create PO 3 with partner in list seller of product in line order
        self.po_3_vals = {
            'partner_id': self.partner_id_1.id,
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

        self.po_3 = self.PurchaseOrder.create(self.po_3_vals)
        self.assertTrue(self.po_3, 'Purchase: no purchase order created')

        # Test edit PO 3 with partner not in list seller of product in line order
        with self.assertRaises(ValidationError):
            self.po_3.write({'partner_id': self.partner_id_2.id})

