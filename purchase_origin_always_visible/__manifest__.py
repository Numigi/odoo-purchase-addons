# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Purchase Origin Always Visible",
    "summary": "Make the source document always visible on purchase orders",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "licence": "AGPL-3",
    "version": "1.0.0",
    "depends": [
        "purchase",
        "base_view_inheritance_extension",
    ],
    "data": [
        "views/purchase_order.xml",
    ],
    "installable": True,
}
