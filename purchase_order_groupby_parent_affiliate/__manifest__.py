# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Purchase Order group by Parent Affiliate",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "Purchase",
    "depends": ["purchase", "partner_affiliate_extended"],
    "summary": "Add the possibility to group by parent affiliate on purchase order.",
    "data": [
        "views/purchase_order_views.xml",
    ],
    "installable": True,
}
