# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)

from odoo import api, models


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
