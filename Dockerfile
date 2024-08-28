FROM python:alpine3.19@sha256:1211782a3ba387d755e0e50cbd40cf771a731d12702e55d46fb74eb2c0254524

RUN apk add --no-cache \
    bash \
    openssh-client \
    curl \
    jq \
    tmux

RUN pip install --no-cache-dir --upgrade ansible==10.3.0 requests==2.32.3 python-dotenv==1.0.1

COPY .ssh /root/.ssh
COPY scripts /root/scripts

RUN ln -s /root/scripts/manage_droplets.py /usr/local/bin/manage_droplets && chmod +x /usr/local/bin/manage_droplets

ENTRYPOINT ["tail", "-f", "/dev/null"]

