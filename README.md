# Telethon reader

## Example configuration
### .env:
```
PHONE=79146842368
SESSION_PATH=/code/sessions/session.session
API_ID=893940
API_HASH=9f6cd16808d2b12b0d3e352677d14448

PROXY_HOST=
PROXY_PORT=
PROXY_USERNAME=
PROXY_PASSWORD=
PROXY_TYPE=
```

## Run from docker
#### First run interactive for authorize
```shell
docker run \
 -it \
 --env-file .env \
 -v telethon-reader-sessions:/code/sessions \
 mailf/telethon-reader
```
