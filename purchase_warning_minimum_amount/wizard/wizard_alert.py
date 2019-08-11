# -*- coding: utf-8 -*-
# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-v3).

from odoo import models, fields, api


class WizardAlert(models.TransientModel):

    _name = 'wizard.alert'

    def _default_order(self):
        self.env['purchase.order'].browse(self._context.get('active_id'))

    order_id = fields.Many2one('purchase.order', string="Purchase Order", default=_default_order)

    @api.multi
    def apply(self):
        context_ = self._context.copy()
        context_.update({'confirm_order': True})
        if context_.get('to_confirm', False):
            return self.order_id.with_context(context_).button_confirm()
        if context_.get('to_approve', False):
            return self.order_id.with_context(context_).button_approve()
