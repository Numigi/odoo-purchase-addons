# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _purchase_service_generation(self):
        company_id = self.mapped("company_id")
        if company_id:
            res = super(
                SaleOrderLine, self.with_context(force_company=company_id[0].id)
            )._purchase_service_generation()
        else:
            res = super(SaleOrderLine, self)._purchase_service_generation()
        return res
