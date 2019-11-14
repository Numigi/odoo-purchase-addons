

def get_products_from_supplier_info(info: 'product.supplier_info') -> 'product.product':
    """Get the products related to the given supplier info recordset.

    :param info: a recordset containing zero to many supplier prices.
    :return: a recordset containing zero to many product variants.
    """
    info_specific_to_variant = info.filtered(lambda i: i.product_id)
    info_not_specific_to_variant = info.filtered(lambda i: not i.product_id)
    return (
        info_specific_to_variant.mapped('product_id') |
        info_not_specific_to_variant.mapped('product_tmpl_id.product_variant_ids')
    )


def get_supplier_info_from_product(product_variant: 'ProductProduct') -> 'product.supplier_info':
    """Get a supplier info recordset from the given product.

    :param product_variant: a product.product singleton.
    :return: a recordset containing zero to many supplier prices.
    """
    product_template_info = product_variant.product_tmpl_id.seller_ids
    return product_template_info.filtered(
        lambda i: not i.product_id or i.product_id == product_variant)
