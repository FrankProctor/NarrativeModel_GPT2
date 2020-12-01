import glob
import click
import os.path
from random import random

ARTICLE_LEN_THRESHOLD = 2048

# only symbol in the map for MacRoman encoding will be kept and mapped
# to UTF-8 counterpart
MAC_ROMAN_UTF8_MAP = dict([
    (0xd0, bytes([0x2d])),
    (0xd1, bytes([0x2d])),
    (0xd2, bytes([0x22])),
    (0xd3, bytes([0x22])),
    (0xd4, bytes([0x27])),
    (0xd5, bytes([0x27])),
    (0xc7, bytes([0xc2, 0xab])),
    (0xc8, bytes([0xc2, 0xbb])),
    (0xc9, bytes([0xe2, 0x80, 0xa6])),
])


def is_big5_at(buf, pos):
    if pos > len(buf) - 2:
        return False

    if buf[pos] >= 0x81 and buf[pos] <= 0xfe:
        if (
            (buf[pos + 1] >= 0x40 and buf[pos + 1] <= 0x7e)
            or (buf[pos+1] >= 0xa1 and buf[pos+1] <= 0xfe)
        ):
            return True

    return False


def process_doc(file_path):
    """
    Text extracted from InDesign has mixed encoding in Big-5 and MacRoman
    process_doc will convert them to utf-8.

    It will also check the text in a document is long enough to exclude those
    non article text.
    """

    buf = bytes()
    pos = 0
    is_prev_big5 = False

    with open(file_path, 'rb') as fp:
        doc = fp.read()

    if len(doc) < ARTICLE_LEN_THRESHOLD:
        return None

    while pos < len(doc):
        cur = doc[pos]
        if cur in MAC_ROMAN_UTF8_MAP.keys():
            if not is_prev_big5 and not is_big5_at(doc, pos + 2):
                buf += MAC_ROMAN_UTF8_MAP[cur]
                pos += 1
                is_prev_big5 = False
                continue

        if is_big5_at(doc, pos):
            pos += 2
            is_prev_big5 = True
        else:
            if cur < 128:
                buf += bytes([cur])
            pos += 1
            is_prev_big5 = False

    if len(buf) < (ARTICLE_LEN_THRESHOLD >> 2):
        return None

    return buf.decode('utf-8')


@click.command()
@click.option(
    'split_ratio', '--split', '-s', type=float, default=0.9,
    help='Ratio between training set and test set'
)
@click.argument(
    'input_dir',
    type=click.Path(exists=True, file_okay=False)
)
def main(split_ratio, input_dir):

    docs = []

    for file in glob.glob(os.path.join(input_dir, '**', '*.txt')):
        doc = process_doc(file)
        if doc is not None:
            docs.append(doc)

    with open('indd.train.txt', 'w') as train_fp, open('indd.test.txt', 'w') as test_fp:
        for doc in docs:
            if random() < 0.9:
                train_fp.write(doc + '\n')
            else:
                test_fp.write(doc + '\n')


if __name__ == '__main__':
    main()
