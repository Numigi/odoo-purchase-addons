FROM quay.io/numigi/odoo-public:14.latest
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
COPY product_supplier_name_search /mnt/extra-addons/product_supplier_name_search
COPY purchase_estimated_time_arrival /mnt/extra-addons/purchase_estimated_time_arrival
COPY purchase_order_groupby_parent_affiliate /mnt/extra-addons/purchase_order_groupby_parent_affiliate
COPY purchase_order_line_price_history_currency /mnt/extra-addons/purchase_order_line_price_history_currency
COPY purchase_partner_products /mnt/extra-addons/purchase_partner_products
COPY purchase_portal_datepicker_overflow /mnt/extra-addons/purchase_portal_datepicker_overflow
COPY purchase_reception_date_enhanced /mnt/extra-addons/purchase_reception_date_enhanced

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
