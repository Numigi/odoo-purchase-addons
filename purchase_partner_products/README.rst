Purchase Partner Products
=========================
This module restricts the selection of products on purchase orders based on the selected supplier.

Usage
-----
As member of ``Purchase / Manager``, I go to the form view of a product.

I add a supplier to the product.

.. image:: static/description/product_form.png

As member of ``Purchase / User``, I create a request for quotation and select a contact.

.. image:: static/description/new_purchase_order.png

I notice that the list of available products is filtered.
Only the products under the commercial entity of the selected contact are available.

.. image:: static/description/purchase_order_product_list_filtered.png

Validation Constraint
---------------------
When the order is confirmed, if the supplier does not match every selected product,
a blocking error message is displayed.

.. image:: static/description/purchase_order_error_message.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
