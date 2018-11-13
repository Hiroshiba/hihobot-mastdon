import fire
from mastodon import Mastodon


def create_app(client_name: str, api_base_url: str, output: str):
    Mastodon.create_app(
        client_name=client_name,
        api_base_url=api_base_url,
        to_file=output,
    )


if __name__ == '__main__':
    fire.Fire(create_app)
