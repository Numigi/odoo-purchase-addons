# -*- coding: utf-8 -*-
# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-v3).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    service_to_purchase = fields.Boolean(company_dependent=True)
