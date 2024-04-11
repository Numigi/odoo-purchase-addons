# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, time

from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _convert_to_middle_of_day(self, date):
        """Return a datetime which is the noon of the input date(time) according
        to order user's time zone, convert to UTC time.
        Input date is in UTC time combined with time(12).

        :param date: datetime
        """
        # Test time is not midnight, then set the time to noon.
        # This is to ensure that we have noon time displayed if the user local browser
        # is the same as the user_id timezone, or company_id timezone (on partner_id).
        # Else, UTC is used for conversion.
        if date.time() == time():
            date = datetime.combine(date, time(12))
        return super(PurchaseOrderLine, self)._convert_to_middle_of_day(date)
