Product Supplier Info Helpers
=============================
This module adds helpers to manipulate product supplier info (supplier prices).

.. contents:: Table of Contents

Context
-------
In Odoo, a supplier price can be defined on a product template or on a variant.

When implementing business logic related to supplier prices, it is sometimes required
to map a product to its prices or the inverse.

This is not a trivial task and can lead to subtile bugs.

Usage
-----

Mapping a Product to Supplier Prices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mapping a product to its supplier prices is done with the function ``get_supplier_info_from_product``.

Here is an example with a purchase order line.

.. code-block:: python

    from odoo.addons.product_supplier_info_helpers.helpers import get_supplier_info_from_product


    class PurchaseOrderLine(models.Model):

        _inherit = 'purchase.order.line'

        def some_business_logic(self):
            supplier_info = get_supplier_info_from_product(self.product_id)

            for info in supplier_info:
                ...


Mapping a Supplier Price to a Product
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A use case of mapping a supplier price to a product is to trigger business logic when a price is updated.

.. code-block:: python

    from odoo.addons.product_supplier_info_helpers.helpers import get_products_from_supplier_info


    class ProductSupplierInfo(models.Model):

        _inherit = 'product.supplier_info'

        def write(self, vals):
            super().write(vals)
            products = get_products_from_supplier_info(self)
            products.apply_some_business_logic()
            return True

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
