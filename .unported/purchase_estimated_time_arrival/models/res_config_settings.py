# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models

DEFAULT_ETA_DAYS = 365
ETA_DAYS_PARAMETER_NAME = "purchase_eta_days"


def get_purchase_eta_days(env) -> int:
    value = env["ir.config_parameter"].sudo().get_param(ETA_DAYS_PARAMETER_NAME)
    return int(value) if value else DEFAULT_ETA_DAYS


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    purchase_eta_days = fields.Integer(
        config_parameter=ETA_DAYS_PARAMETER_NAME, default=DEFAULT_ETA_DAYS
    )
