FROM quay.io/numigi/odoo-public:12.latest
LABEL maintainer="contact@numigi.com"

USER odoo

COPY purchase_partner_products /mnt/extra-addons/purchase_partner_products
COPY purchase_warning_minimum_amount /mnt/extra-addons/purchase_warning_minimum_amount

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
