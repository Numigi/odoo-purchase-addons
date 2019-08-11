# -*- coding: utf-8 -*-
# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-v3).

from odoo import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    min_purchase_amount = fields.Float(string="Minimum Purchase amount")
