# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):

    _inherit = "product.category"

    consignment_delivery_expense = fields.Boolean(
        "Automated Expense on Delivery", company_dependent=True
    )
    consignment_delivery_expense_account_id = fields.Many2one(
        "account.account", domain=[("deprecated", "=", False)], company_dependent=True
    )
    consignment_delivery_transit_account_id = fields.Many2one(
        "account.account", domain=[("deprecated", "=", False)], company_dependent=True
    )
    consignment_delivery_journal_id = fields.Many2one(
        "account.journal", company_dependent=True
    )

    @api.constrains("consignment_delivery_expense", "property_valuation")
    def _check_consignment_delivery_expense_versus_valuation(self):
        for category in self:
            if (
                category.consignment_delivery_expense
                and category.property_valuation == "real_time"
            ):
                raise ValidationError(
                    _(
                        "The automated expense on delivery option is incompatible with "
                        "the automated inventory valuation."
                    )
                )

    @api.constrains("consignment_delivery_expense", "property_cost_method")
    def _check_consignment_delivery_expense_versus_cost_method(self):
        for category in self:
            if (
                category.consignment_delivery_expense
                and category.property_cost_method != "standard"
            ):
                raise ValidationError(
                    _(
                        "The automated expense on delivery option is only compatible with "
                        "the standard price cost method."
                    )
                )

    @api.constrains("consignment_delivery_expense", "consignment")
    def _check_consignment_delivery_expense_versus_consignment(self):
        for category in self:
            if category.consignment_delivery_expense and not category.consignment:
                raise ValidationError(
                    _(
                        "The automated expense on delivery option is only compatible with "
                        "consignment categories."
                    )
                )
