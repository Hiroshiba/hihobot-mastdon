import re
from pathlib import Path
from typing import Optional

import fire
from hihobot.hihobot import Hihobot
from mastodon import Mastodon, StreamListener

import time


def _remove_html_tag(text: str, _re=re.compile(r'<[^>]*?>')):
    return _re.sub('', text)


def _remove_mention_word(text: str, _re=re.compile(r'(\s+)?@\w+(\s+)?')):
    return _re.sub('', text)


def _random_toot(
        mastodon: Mastodon,
        hihobot: Hihobot,
):
    toot = mastodon.timeline_local(limit=1)[0]
    in_text = _remove_html_tag(toot['content'])

    vec = hihobot.text_to_vec(in_text)
    out_text = hihobot.generate(vec=vec)
    mastodon.status_post(out_text)


def run_random_toot(
        time_span: float,
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
    assert time_span >= 60, 'wait! time_span is very short!'

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

    while True:
        _random_toot(mastodon=mastodon, hihobot=hihobot)
        time.sleep(time_span)


if __name__ == '__main__':
    fire.Fire(run_random_toot)
