# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class InvoiceFromPickingCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env['res.partner'].create({
            'name': 'Supplier',
            'supplier': True,
        })

        cls.product_a = cls.env['product.product'].create({
            'name': 'Product A',
        })

        cls.product_b = cls.env['product.product'].create({
            'name': 'Product B',
        })

        cls.expense_account = cls.env['account.account'].create({
            'name': 'Expense',
            'code': '511001',
            'user_type_id': cls.env.ref('account.data_account_type_expenses').id,
        })
        cls.payable_account = cls.env['account.account'].create({
            'name': 'Payable',
            'code': '211001',
            'user_type_id': cls.env.ref('account.data_account_type_payable').id,
            'reconcile': True,
        })

        cls.invoice = cls.env['account.invoice'].create({
            'type': 'in_invoice',
            'partner_id': cls.supplier.id,
            'account_id': cls.payable_account.id,
            'origin': 'PO00079',
            'invoice_line_ids': [
                (0, 0, {
                    'name': cls.product_a.display_name,
                    'product_id': cls.product_a.id,
                    'product_uom': cls.product_a.uom_id.id,
                    'quantity': 1,
                    'price_unit': 100,
                    'account_id': cls.expense_account.id,
                }),
                (0, 0, {
                    'name': cls.product_b.display_name,
                    'product_id': cls.product_b.id,
                    'product_uom': cls.product_b.uom_id.id,
                    'quantity': 1,
                    'price_unit': 100,
                    'account_id': cls.expense_account.id,
                }),
            ]
        })

    def test_after_button_click__origin_emptied(self):
        self.invoice.empty_supplier_invoice_lines()
        assert not self.invoice.origin

    def test_after_button_click__invoice_lines_deleted(self):
        self.invoice.empty_supplier_invoice_lines()
        assert not self.invoice.invoice_line_ids
