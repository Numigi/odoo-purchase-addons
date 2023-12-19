# © 2019 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Main Module",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Install all addons required for testing.",
    "depends": [
        # "sale_stock",  # required for testing purchase_consignment_delivery_expense
        # "onchange_helper",  # used for testing purchase_consignment
        "product_supplier_info_helpers",
        "product_supplier_name_search",
        # "purchase_consignment",
        # "purchase_consignment_delivery_expense",
        # "purchase_consignment_inventory",
        "purchase_estimated_time_arrival",
        "purchase_order_groupby_parent_affiliate",
        "purchase_order_line_price_history_currency",
        # "purchase_invoice_empty_lines",
        # "purchase_invoice_from_picking",
        # "purchase_line_editable_list",
        # "purchase_origin_always_visible",
        "purchase_partner_products",
        # "purchase_warning_minimum_amount",
        # "stock_block_auto_purchase_order",
        # "stock_orderpoint_editable_list",
        # "stock_picking_groupby_purchase_user",
        # "stock_picking_supplier_reference",
    ],
    "installable": True,
}
