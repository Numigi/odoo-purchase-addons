# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta
from odoo import fields, models, _
from typing import Mapping
from .res_config_settings import get_purchase_eta_days


def aggregate_average_eta(
    products: 'product.product',
    group_by_field: str = 'product_id',
) -> Mapping[int, float]:
    """Aggregate the average of ETA days for the given products.

    :param products: the products for which to aggregate the ETA.
    :param group_by_field: the field to group by to aggregate the ETA.
        This must be an existing Many2one field of stock.arrival.time.
    """
    env = products.env
    min_receipt_date = datetime.now() - timedelta(get_purchase_eta_days(env))
    eta_domain = [
        ('product_id', 'in', products.ids),
        ('receipt_date', '>=', min_receipt_date),
    ]
    eta_data = env['stock.arrival.time'].read_group(
        eta_domain, [group_by_field, 'days'], [group_by_field]
    )
    return {r[group_by_field][0]: r['days'] for r in eta_data}


def _get_eta_details_action(context: dict) -> dict:
    return {
        'name': _('ETA'),
        'type': 'ir.actions.act_window',
        'res_model': 'stock.arrival.time',
        'view_type': 'form',
        'view_mode': 'list',
        'target': 'current',
    }


class ProductProduct(models.Model):

    _inherit = "product.product"

    eta = fields.Float(compute='_compute_eta', string='ETA')

    def _compute_eta(self):
        eta_data_dict = aggregate_average_eta(self)

        for product in self:
            product.eta = eta_data_dict.get(product.id, 0)

    def action_open_eta_details(self):
        action = _get_eta_details_action(self._context)
        action['context'] = dict(self._context, search_default_product_id=self.id)
        return action


class ProductTemplate(models.Model):

    _inherit = "product.template"

    eta = fields.Float(compute='_compute_eta')

    def _compute_eta(self):
        variants = self.mapped('product_variant_ids')
        eta_data_dict = aggregate_average_eta(variants, 'product_tmpl_id')

        for product_template in self:
            product_template.eta = eta_data_dict.get(product_template.id, 0)

    def action_open_eta_details(self):
        action = _get_eta_details_action(self._context)
        action['context'] = dict(self._context, search_default_product_tmpl_id=self.id)
        return action
