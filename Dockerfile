FROM quay.io/numigi/odoo-public:11.latest
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

COPY purchase_invoice_empty_lines /mnt/extra-addons/purchase_invoice_empty_lines
COPY purchase_invoice_from_picking /mnt/extra-addons/purchase_invoice_from_picking
COPY stock_picking_supplier_reference /mnt/extra-addons/stock_picking_supplier_reference

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
