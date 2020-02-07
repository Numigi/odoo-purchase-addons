# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.exceptions import ValidationError
from .common import get_products_from_supplier_id


class StockInventory(models.Model):

    _inherit = 'stock.inventory'

    def action_validate(self):
        for line in self.mapped('line_ids'):
            line.check_selected_owner()
        return super().action_validate()


class StockInventoryLine(models.Model):

    _inherit = 'stock.inventory.line'

    def check_selected_owner(self):
        inventoried_owner = self._get_inventoried_owner()
        if inventoried_owner:
            self._check_has_the_inventoried_owner(inventoried_owner)

    def _check_has_the_inventoried_owner(self, inventoried_owner):
        if inventoried_owner != self.partner_id:
            raise ValidationError(_(
                "The owner / supplier selected on the inventory ({}) "
                "must be selected on each inventory line."
            ).format(inventoried_owner.display_name))

    def check_selected_product(self):
        super().check_selected_product()

        inventoried_owner = self._get_inventoried_owner()
        if inventoried_owner:
            self._check_product_has_owner(inventoried_owner)

    def _get_inventoried_owner(self):
        return self.inventory_id.partner_id or self.inventory_id.consignment_supplier_id

    def _check_product_has_owner(self, inventoried_owner):
        allowed_products = get_products_from_supplier_id(self.env, inventoried_owner.id)
        if self.product_id not in allowed_products:
            raise ValidationError(_(
                "The product selected on the inventory line ({product}) "
                "does not belong to the selected owner / supplier ({owner})."
            ).format(
                product=self.product_id.display_name,
                owner=inventoried_owner.display_name,
            ))
