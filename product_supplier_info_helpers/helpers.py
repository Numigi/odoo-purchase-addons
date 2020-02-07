

def get_products_from_supplier_info(info: 'product.supplierinfo') -> 'product.product':
    """Get the products related to the given supplier info recordset.

    :param info: a recordset containing zero to many supplier prices.
    :return: a recordset containing zero to many product variants.
    """
    info_specific_to_variant = info.filtered(lambda i: i.product_id)
    info_not_specific_to_variant = info.filtered(lambda i: not i.product_id)
    return (
        _supplier_info_to_single_variant(info_specific_to_variant) |
        _supplier_info_to_all_variants(info_not_specific_to_variant)
    )


def get_supplier_info_from_product(product_variant: 'ProductProduct') -> 'product.supplierinfo':
    """Get a supplier info recordset from the given product.

    :param product_variant: a product.product singleton.
    :return: a recordset containing zero to many supplier prices.
    """
    product_template_info = product_variant.product_tmpl_id.seller_ids
    return product_template_info.filtered(
        lambda i: not i.product_id or i.product_id == product_variant)


def _supplier_info_to_single_variant(info):
    return info.mapped('product_id')


def _supplier_info_to_all_variants(info):
    """Get all product variants related to a supplier price.

    This is done in an SQL query to avoid infinite recursion
    when navigating through the orm.
    """
    if not info:
        return info.env['product.product']

    info._cr.execute("""
        SELECT prod.id
        FROM product_product prod
        JOIN product_template template ON prod.product_tmpl_id = template.id
        JOIN product_supplierinfo info ON info.product_tmpl_id = template.id
        WHERE prod.active is true AND template.active is true
        AND info.id in %s
    """, (tuple(info.ids), ))
    ids = [r[0] for r in info._cr.fetchall()]
    return info.env['product.product'].browse(ids)
