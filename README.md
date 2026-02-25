# shakespearean-insult-api

API returning random Shakespearean insults

## Deployment

On the self-hosted runner, CI builds `flask-service:latest` and deploys it with `docker compose` using `compose.yaml` on pushes to `main`.
