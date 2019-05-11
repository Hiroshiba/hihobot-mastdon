import re
import time
from pathlib import Path
from typing import Optional

import fire
from hihobot.hihobot import Hihobot
from mastodon import Mastodon, StreamListener


def _remove_html_tag(text: str, _re=re.compile(r'<[^>]*?>')):
    return _re.sub('', text)


def _remove_mention_word(text: str, _re=re.compile(r'(\s+)?@\w+(\s+)?')):
    return _re.sub('', text)


class Runner(StreamListener):
    def __init__(
            self,
            mastodon: Mastodon,
            hihobot: Hihobot,
            wait_span: float,
    ):
        self.mastodon = mastodon
        self.hihobot = hihobot
        self.wait_span = wait_span

        self.me = mastodon.account_verify_credentials()

    def _reply(self, text: str, in_reply_to_id):
        time.sleep(self.wait_span)
        self.mastodon.status_post(text, in_reply_to_id=in_reply_to_id)

    def on_notification(self, notification):
        try:
            if notification.type != 'mention':
                return

            toot = notification.status

            from_username = toot.account.username
            if self.me.username == from_username:
                return

            if toot.account.bot:
                return

            in_text = _remove_mention_word(_remove_html_tag(toot['content']))

            vec = self.hihobot.text_to_vec(in_text)
            out_text = self.hihobot.generate(vec=vec)
            out_text = f'@{from_username} {out_text}'

            self._reply(out_text, in_reply_to_id=toot)
        except:
            import traceback
            traceback.print_exc()

    def run(self):
        print('running...', flush=True)
        self.mastodon.stream_user(self)


def run_auto_reply(
        wait_span: float,
        token_path: str,
        mastodon_url: str,
        model_path: str,
        model_config: str,
        char_path: str,
        doc2vec_model_path: str,
        max_length: int,
        sampling_maximum: bool,
        gpu: Optional[int],
):
    mastodon = Mastodon(
        access_token=token_path,
        api_base_url=mastodon_url,
    )
    hihobot = Hihobot(
        model_path=Path(model_path),
        model_config=Path(model_config),
        char_path=Path(char_path),
        doc2vec_model_path=Path(doc2vec_model_path),
        max_length=max_length,
        sampling_maximum=sampling_maximum,
        gpu=gpu,
    )
    runner = Runner(
        mastodon=mastodon,
        hihobot=hihobot,
        wait_span=wait_span,
    )
    runner.run()


if __name__ == '__main__':
    fire.Fire(run_auto_reply)
