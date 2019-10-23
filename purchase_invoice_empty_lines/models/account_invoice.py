# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    def empty_supplier_invoice_lines(self):
        self.invoice_line_ids.unlink()
        self.origin = False
