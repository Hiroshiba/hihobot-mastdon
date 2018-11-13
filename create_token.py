import fire
from mastodon import Mastodon


def create_token(
        app_file: str,
        api_base_url: str,
        username: str,
        password: str,
        output: str,
):
    mastodon = Mastodon(
        client_id=app_file,
        api_base_url=api_base_url,
    )
    mastodon.log_in(
        username=username,
        password=password,
        to_file=output,
    )


if __name__ == '__main__':
    fire.Fire(create_token)
