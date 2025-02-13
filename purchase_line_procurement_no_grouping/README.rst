Purchase Line Procurement No Grouping
=====================================

This module prevent grouping purchase order lines coming from different progurement group. 
This module works only for products with route "Replenish on Order (MTO)" configured as inventory operations.

How it works:
=============

I create a new product:

.. image:: static/description/storable_product.png

I set a vendor fot my product:

.. image:: static/description/product_vendor.png

I check the route `Replenish on Order (MTO)` (This route is archived by default so make sure to activate it):

.. image:: static/description/product_mto_route.png

I create a sale order for my product and I confirm it:

.. image:: static/description/sale_order_1.png

A purchase order is generated for my sale order:

.. image:: static/description/purchase_order_1.png

I go back to sale application, to create a new sale order for my product and I confirm it:

.. image:: static/description/sale_order_2.png

I go to the linked purchase order, I can see that a new line is added in the previous purchase order for the same product. 

.. image:: static/description/purchase_order_2.png

The lines are note grouped because the procurement group is different. 

Without this module installed, the purchase order lines will be merget into one line by cummulating quantities. 


Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
