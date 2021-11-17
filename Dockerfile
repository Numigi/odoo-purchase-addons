FROM quay.io/numigi/odoo-public:12.latest
LABEL maintainer="contact@numigi.com"

USER root

ARG GIT_TOKEN

COPY .docker_files/test-requirements.txt ./test-requirements.txt
RUN pip3 install -r ./test-requirements.txt && rm ./test-requirements.txt

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY product_supplier_info_helpers /mnt/extra-addons/product_supplier_info_helpers
COPY purchase_consignment /mnt/extra-addons/purchase_consignment
COPY purchase_consignment_delivery_expense /mnt/extra-addons/purchase_consignment_delivery_expense
COPY purchase_consignment_inventory /mnt/extra-addons/purchase_consignment_inventory
COPY purchase_estimated_time_arrival /mnt/extra-addons/purchase_estimated_time_arrival
COPY purchase_invoice_empty_lines /mnt/extra-addons/purchase_invoice_empty_lines
COPY purchase_invoice_from_picking /mnt/extra-addons/purchase_invoice_from_picking
COPY purchase_line_editable_list /mnt/extra-addons/purchase_line_editable_list
COPY purchase_origin_always_visible /mnt/extra-addons/purchase_origin_always_visible
COPY purchase_partner_products /mnt/extra-addons/purchase_partner_products
COPY purchase_warning_minimum_amount /mnt/extra-addons/purchase_warning_minimum_amount
COPY stock_block_auto_purchase_order /mnt/extra-addons/stock_block_auto_purchase_order
COPY stock_orderpoint_editable_list /mnt/extra-addons/stock_orderpoint_editable_list
COPY stock_picking_groupby_purchase_user /mnt/extra-addons/stock_picking_groupby_purchase_user
COPY stock_picking_supplier_reference /mnt/extra-addons/stock_picking_supplier_reference

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
