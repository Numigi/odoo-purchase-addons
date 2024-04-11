# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo.tests import tagged, Form
from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install")
class TestPurchaseOrderUpdate(AccountTestInvoicingCommon):
    def test_convert_to_middle_of_day(self):
        """Test the method _convert_to_middle_of_day."""
        updated_dates = []
        po = Form(self.env["purchase.order"])
        po.partner_id = self.partner_a
        with po.order_line.new() as po_line:
            po_line.product_id = self.product_a
            po_line.product_qty = 1
            po_line.price_unit = 100
        with po.order_line.new() as po_line:
            po_line.product_id = self.product_b
            po_line.product_qty = 10
            po_line.price_unit = 200
        po = po.save()
        po.user_id.tz = "Canada/Eastern"

        # We use a date without time, so it should be converted to noon
        # Portal date do not have time.
        date = datetime.strptime("2024-03-27", "%Y-%m-%d")

        converted_date = po.order_line[0]._convert_to_middle_of_day(date)
        self.assertEqual(
            converted_date,
            datetime.strptime("2024-03-27 16:00:00", "%Y-%m-%d %H:%M:%S"),
        )
        updated_dates.append((po.order_line[0], converted_date))
        # Database date is in UTC time
        # When displayed on local browser, it will be converted to the user's timezone
        # The date will be displayed as 2024-03-27 12:00:00
        # for the user located in Canada/Eastern
        # So for that datetime if user is located in Shanghai UTC+8,
        # it will be displayed as 2024-03-28 00:00:00
        if updated_dates:
            po._update_date_planned_for_lines(updated_dates)
        self.assertEqual(
            po.date_planned,
            datetime.strptime("2024-03-27 16:00:00", "%Y-%m-%d %H:%M:%S"),
        )
