# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestPurchaseOrder(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_1 = cls.env['res.partner'].create({
            'name': 'My Partner Company 1',
            'is_company': True,
        })
        cls.contact_1 = cls.env['res.partner'].create({
            'name': 'My Contact 1',
            'is_company': False,
            'parent_id': cls.partner_1.id,
        })

        cls.partner_2 = cls.env['res.partner'].create({
            'name': 'My Partner Company 2',
            'is_company': True,
        })

        cls.product_categ = cls.env.ref('product.product_category_5')
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')

        cls.product_1 = cls.env['product.product'].create(cls._get_product_vals(cls.partner_1))
        cls.product_2 = cls.env['product.product'].create(cls._get_product_vals(cls.partner_2))
        product_attribute = cls.env['product.attribute'].create({'name': 'Size'})
        size_value_l = cls.env['product.attribute.value'].create([{
            'name': 'L',
            'attribute_id': product_attribute.id,
        }])
        size_value_s = cls.env['product.attribute.value'].create([{
            'name': 'S',
            'attribute_id': product_attribute.id,
        }])

        cls.template_a = cls.env['product.template'].create(
            cls._get_product_vals(cls.partner_1)
        )
        cls.env['product.template.attribute.line'].create({
            'attribute_id': product_attribute.id,
            'product_tmpl_id': cls.template_a.id,
            'value_ids': [(6, 0, [size_value_s.id, size_value_l.id])],
        })
        cls.variant_a1 = cls.template_a.product_variant_ids[0]
        cls.variant_a2 = cls.template_a.product_variant_ids[1]
        cls.order = cls.env['purchase.order'].create({
            'partner_id': cls.partner_1.id,
            'order_line': [],
        })

    @classmethod
    def _get_product_vals(cls, suppliers):
        return {
            'name': 'Acier Lac 3.4',
            'categ_id': cls.product_categ.id,
            'type': 'consu',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'default_code': 'ACIERLC3',
            'seller_ids': [
                (0, 0, {'name': p.id}) for p in suppliers
            ]
        }

    @classmethod
    def _get_po_line_vals(cls, product):
        return {
            'name': product.name,
            'product_id': product.id,
            'product_qty': 6.0,
            'product_uom': product.uom_po_id.id,
            'price_unit': 100.0,
            'date_planned': datetime.now(),
        }

    def confirm_order(self):
        self.order.with_context(force_apply_purchase_partner_products=True).button_confirm()

    def test_if_one_product_with_same_partner__error_not_raised(self):
        self.order.write({'order_line': [(0, 0, self._get_po_line_vals(self.product_1))]})
        self.confirm_order()

    def test_if_two_products_with_same_partner__error_not_raised(self):
        self.order.write({'order_line': [
            (0, 0, self._get_po_line_vals(self.product_1)),
            (0, 0, self._get_po_line_vals(self.product_1)),
        ]})
        self.confirm_order()

    def test_if_one_product_with_child_partner__error_not_raised(self):
        self.order.write({'order_line': [(0, 0, self._get_po_line_vals(self.product_1))]})
        self.order.partner_id = self.contact_1
        self.confirm_order()

    def test_if_one_product_unrelated_partner__error_raised(self):
        self.order.write({'order_line': [(0, 0, self._get_po_line_vals(self.product_2))]})
        with pytest.raises(ValidationError):
            self.confirm_order()

    def test_if_partner_defined_on_variant__error_raised(self):
        template = self.product_1.product_tmpl_id

        product_2 = self.product_1.copy()
        product_2.product_tmpl_id = template.id
        template.seller_ids.product_id = self.product_1

        self.order.write({'order_line': [(0, 0, self._get_po_line_vals(self.product_1))]})
        self.confirm_order()

    def test_if_partner_defined_on_other_variant__error_raised(self):
        self.variant_a2.seller_ids = [(5, 0, 0)]
        self.variant_a2.seller_ids = [(1, 0, {'name': self.partner_2.id})]
        self.order.write({'order_line': [(0, 0, self._get_po_line_vals(self.variant_a1))]})
        with pytest.raises(ValidationError):
            self.confirm_order()
