Purchase Invoice Ref Stop Propagate
==================================
This module prevents the automatic propagation of the purchase order reference to the invoice reference and payment reference when creating an invoice from a purchase order.

By default in Odoo, when creating a vendor bill from a purchase order,
the vendor reference (`partner_ref`) is automatically copied to:

- The invoice reference field (`ref`)
- The payment reference field (`payment_ref`)

This module disables that behavior, allowing users to manually set the invoice reference.

Before Applying the Module
--------------------------
When creating a vendor bill from a purchase order, the vendor reference from the purchase order
is automatically copied to the invoice reference (`ref`) and payment reference (`payment_ref`) fields.


After Applying the Module
-------------------------
With this module installed, the invoice reference (`ref`) and payment reference (`payment_ref`) fields
remain empty, preventing automatic propagation of vendor reference from the purchase order.

.. image:: https://raw.githubusercontent.com/Numigi/odoo-purchase-addons/14.0/purchase_invoice_ref_stop_propagate/static/description/vendor_bills.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
