import argparse

from telethon import TelegramClient, utils, events
from loguru import logger


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
    parser.add_argument('phone', help="Telegram phone", type=int)
    parser.add_argument('session-path', help="Path to .session")
    parser.add_argument('api-id', help="App api_id from https://my.telegram.org/apps", type=int)
    parser.add_argument('api-hash', help="App api_hash from https://my.telegram.org/apps")

    parser.add_argument('--proxy-host')
    parser.add_argument('--proxy-port')
    parser.add_argument('--proxy-username')
    parser.add_argument('--proxy-password')
    parser.add_argument('--proxy-type')

    args = vars(parser.parse_args())

    proxy = {
        "proxy_type": args['proxy_type'],
        "addr": args['proxy_host'],
        "port": args['proxy_port'],
        "user": args['proxy_username'],
        "pass": args['proxy_password'],
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
