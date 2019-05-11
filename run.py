import threading
from time import sleep
from typing import List, Optional

import fire

from run_auto_myname import run_auto_myname
from run_auto_reply import run_auto_reply
from run_random_toot import run_random_toot


def run(
        time_span: float,
        wait_span: float,
        myname_list: List[str],
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
    thread_auto_myname = threading.Thread(target=run_auto_myname, kwargs=dict(
        wait_span=wait_span,
        myname_list=myname_list,
        token_path=token_path,
        mastodon_url=mastodon_url,
        model_path=model_path,
        model_config=model_config,
        char_path=char_path,
        doc2vec_model_path=doc2vec_model_path,
        max_length=max_length,
        sampling_maximum=sampling_maximum,
        gpu=gpu,
    ))
    thread_auto_myname.start()
    sleep(3)

    thread_auto_reply = threading.Thread(target=run_auto_reply, kwargs=dict(
        wait_span=wait_span,
        token_path=token_path,
        mastodon_url=mastodon_url,
        model_path=model_path,
        model_config=model_config,
        char_path=char_path,
        doc2vec_model_path=doc2vec_model_path,
        max_length=max_length,
        sampling_maximum=sampling_maximum,
        gpu=gpu,
    ))
    thread_auto_reply.start()
    sleep(3)

    thread_random_toot = threading.Thread(target=run_random_toot, kwargs=dict(
        time_span=time_span,
        token_path=token_path,
        mastodon_url=mastodon_url,
        model_path=model_path,
        model_config=model_config,
        char_path=char_path,
        doc2vec_model_path=doc2vec_model_path,
        max_length=max_length,
        sampling_maximum=sampling_maximum,
        gpu=gpu,
    ))
    thread_random_toot.start()
    sleep(3)

    thread_auto_myname.join()
    thread_auto_reply.join()
    thread_random_toot.join()


if __name__ == '__main__':
    fire.Fire(run)
