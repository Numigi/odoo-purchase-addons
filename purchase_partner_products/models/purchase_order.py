# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, exceptions, _


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.multi
    def write(self, value):
        if 'partner_id' in value:
            for line in self.order_line:
                valid = any(s for s in line.product_id.seller_ids if s.name.id == value['partner_id'])

                if not valid:
                    partner_obj = self.env['res.partner'].browse(value['partner_id'])
                    raise exceptions.ValidationError(_("Product %s is not allowed for the supplier %s."
                                                     "\nPlease contact your manager.") %
                                                     (line.product_id.name, partner_obj.name))
        return super(PurchaseOrder, self).write(value)


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    @api.model
    def create(self, value):
        if 'order_id' in value and 'product_id' and value:
            product_obj = self.env['product.product'].browse(value['product_id'])
            partner_id = self.env['purchase.order'].browse(value['order_id']).partner_id
            valid = any(s for s in product_obj.seller_ids if s.name.id == partner_id.id)
            if not valid:
                raise exceptions.ValidationError(
                    _("Product %s is not allowed for the supplier %s.\nPlease contact your manager.") % (
                        product_obj.name, partner_id.name))
        return super(PurchaseOrderLine, self).create(value)
