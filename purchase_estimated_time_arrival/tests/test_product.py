# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo.tests.common import SavepointCase

from ..models.res_config_settings import ETA_DAYS_PARAMETER_NAME


def _generate_eta_entry(product, eta_days, receipt_date=None):
    receipt_date = receipt_date or datetime.now()
    product.env["stock.arrival.time"].sudo().create(
        {
            "product_id": product.id,
            "purchase_date": receipt_date - timedelta(eta_days),
            "receipt_date": receipt_date,
        }
    )


class TestProduct(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product A",
                "type": "product",
            }
        )

        cls.limit_in_days = 100
        cls.env["ir.config_parameter"].set_param(
            ETA_DAYS_PARAMETER_NAME, cls.limit_in_days
        )

        cls.product = cls.product.sudo(cls.env.ref("base.user_demo"))

    def test_if_no_eta_lines__eta_is_zero(self):
        assert self.product.eta == 0

    def test_if_multiple_eta_entries__eta_is_average(self):
        _generate_eta_entry(self.product, 3)
        _generate_eta_entry(self.product, 5)
        assert round(self.product.eta, 2) == 4  # (3 + 5) / 2

    def test_products_received_before_limit_excluded(self):
        receipt_date = datetime.now() - timedelta(self.limit_in_days + 1)
        _generate_eta_entry(self.product, 3, receipt_date)
        assert self.product.eta == 0

    def test_products_received_after_limit_excluded(self):
        receipt_date = datetime.now() - timedelta(self.limit_in_days - 1)
        _generate_eta_entry(self.product, 3, receipt_date)
        assert self.product.eta == 3


class TestProductTemplate(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env["product.template"].create(
            {
                "name": "Product Template A",
            }
        )
        cls.variant_1 = cls.template.product_variant_ids[0]
        cls.variant_2 = cls.template.product_variant_ids[1]

        cls.other_product = cls.env["product.product"].create(
            {
                "name": "Variant 1",
                "type": "product",
            }
        )

    def test_product_template_eta_is_average_of_variants(self):
        _generate_eta_entry(self.other_product, 50)  # should not impact the result

        _generate_eta_entry(self.variant_1, 3)
        _generate_eta_entry(self.variant_2, 5)
        assert round(self.template.eta, 2) == 4  # (3 + 5) / 2
