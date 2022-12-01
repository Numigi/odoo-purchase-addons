Stock Inventory Line Product Domain
===================================
This module is a binding between `purchase_consignment_inventory` and `stock_inventory_line_domain <https://github.com/Numigi/odoo-stock-addons/tree/12.0/stock_inventory_line_domain>`_.

.. contents:: Table of Contents

Filter by Owner / Proprietary
-----------------------------
When running an inventory for a single owner / proprietary number, only the products having this partner has supplier are selectable.

Inventory Validation
--------------------
When validating the inventory, a blocking message will be shown if an inventory line does
not match the selected owner / supplier on the inventory adjustment.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
