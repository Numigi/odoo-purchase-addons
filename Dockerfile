FROM quay.io/numigi/odoo-public:12.latest
LABEL maintainer="contact@numigi.com"

USER odoo


COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
