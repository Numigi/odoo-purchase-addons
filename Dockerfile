FROM quay.io/numigi/odoo-public:12.latest
LABEL maintainer="contact@numigi.com"

USER root


COPY .docker_files/test-requirements.txt .
RUN pip3 install -r ./test-requirements.txt && rm ./test-requirements.txt

USER odoo

COPY purchase_consignment /mnt/extra-addons/purchase_consignment
COPY purchase_consignment_inventory /mnt/extra-addons/purchase_consignment_inventory
COPY purchase_invoice_empty_lines /mnt/extra-addons/purchase_invoice_empty_lines
COPY purchase_partner_products /mnt/extra-addons/purchase_partner_products
COPY purchase_warning_minimum_amount /mnt/extra-addons/purchase_warning_minimum_amount

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
