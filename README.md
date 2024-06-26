# smtp2webhook

Smtp server that forwards mail to discord via webhooks

# Deploy with docker

This app is available through the image tag `ghcr.io/waicool20/smtp2webhook:main`

You can also clone this repo, modify the `WEBHOOK_URL` and run `docker compose up -d`

or use this docker compose file

```yml
services:
  smtp2webhook:
    image: ghcr.io/waicool20/smtp2webhook:main
    container_name: smtp2webhook
    restart: always
    ports:
      - "8025:8025"
    environment:
      WEBHOOK_URL: https://discord.com/api/webhooks/... # Set this to discord webhook url    (required)
      MSG_USERNAME: Smtp2Webhook                        # Override for webhook user          (optional)
      HOSTNAME: 0.0.0.0                                 # Override for hostname to listen to (optional)
      PORT: 8025                                        # Override for port to listen to     (optional)
```

# Security

This app has no security at all and is expected to run on a local network that is secured