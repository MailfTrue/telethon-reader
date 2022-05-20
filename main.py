import os
import argparse

from telethon import TelegramClient, utils, events
from loguru import logger


class EnvDefault(argparse.Action):
    def __init__(self, env_var, required=True, default=None, **kwargs):
        if not default and env_var:
            if env_var in os.environ:
                default = os.environ[env_var]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required,
                                         **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def get_client(session_path: str, api_id: int, api_hash: str, proxy: dict = None):
    client = TelegramClient(
        session_path,
        api_id,
        api_hash,
        proxy=proxy
    )

    @client.on(events.NewMessage())
    async def handler(event):
        peer_id = utils.get_peer_id(event.message.peer_id)
        logger.info("New message, "
                    f"Peer: {peer_id}, "
                    f"Text: {event.text}")

    return client


def main():
    parser = argparse.ArgumentParser(description='Telegram reader')
    parser.add_argument('phone', help="Telegram phone", action=EnvDefault, env_var="PHONE", type=int)
    parser.add_argument('session-path', action=EnvDefault, env_var="SESSION_PATH", help="Path to .session")
    parser.add_argument('api-id', action=EnvDefault, env_var="API_ID",
                        help="App api_id from https://my.telegram.org/apps", type=int)
    parser.add_argument('api-hash', action=EnvDefault, env_var="API_HASH",
                        help="App api_hash from https://my.telegram.org/apps")

    parser.add_argument('--proxy-host', action=EnvDefault, env_var="PROXY_HOST", required=False)
    parser.add_argument('--proxy-port', action=EnvDefault, env_var="PROXY_PORT", required=False)
    parser.add_argument('--proxy-username', action=EnvDefault, env_var="PROXY_USERNAME", required=False)
    parser.add_argument('--proxy-password', action=EnvDefault, env_var="PROXY_PASSWORD", required=False)
    parser.add_argument('--proxy-type', action=EnvDefault, env_var="PROXY_TYPE", required=False)

    args = vars(parser.parse_args())

    proxy = {
        "proxy_type": args['proxy_type'],
        "addr": args['proxy_host'],
        "port": args['proxy_port'],
        "username": args['proxy_username'],
        "password": args['proxy_password'],
    } if all(args[k] for k in args if k.startswith("proxy")) else None

    client = get_client(
        session_path=args['session-path'],
        api_id=args['api-id'],
        api_hash=args['api-hash'],
        proxy=proxy
    )
    client.start(phone=args['phone'])
    logger.info(f"Run client with phone: {args['phone']}")
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
