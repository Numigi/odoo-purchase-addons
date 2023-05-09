Purchase Order Line Price History Currency
==========================================
This module adds currency to purchase price history.

.. contents:: Table of Contents

Context
-------
In Odoo, buyers need to see an item's purchase price history on other purchase/order requests so that they can negotiate prices well.

The customer uses the <a href="https://github.com/OCA/purchase-workflow/blob/14.0/purchase_order_line_price_history">purchase_order_line_price_history</a> module which allows to consult the purchase history of an item from a purchase line.

Usage
-----

As a user with access to the Purchase application, I create a new price request and select an item. I click on the ``Price History`` button.

    .. image:: static/description/purchase_order_price_history.png

In the window that appears, I see that a new ``Currency`` column is present.

    .. image:: static/description/purchase_history_currency.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
