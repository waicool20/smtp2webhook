FROM python:alpine3.12

LABEL org.opencontainers.image.authors="waicool20@gmail.com"
LABEL org.opencontainers.image.description="Smtp server that forwards mail to discord via webhooks"
LABEL org.opencontainers.image.licenses="GPL 3.0"
LABEL org.opencontainers.image.source="https://github.com/waicool20/smtp2webhook"
LABEL org.opencontainers.image.title="Smtp2Webhook"

ADD main.py .
RUN pip install requests aiosmtpd
ENTRYPOINT [ "python", "-u" ]
CMD [ "main.py" ]
EXPOSE 8025