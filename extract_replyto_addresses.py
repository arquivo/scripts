import mailbox
import re

import fire


def get_from_addr(mailbox_path):
    for message in mailbox.mbox(mailbox_path):
        for t in message._headers:
            if t[0] == 'Reply-To':
                match = re.search(r'[\w\.-]+@[\w\.-]+', t[1])
                if match:
                    reply_adr = match.group(0)
                    print(reply_adr)
                break


if __name__ == '__main__':
    fire.Fire(get_from_addr)
