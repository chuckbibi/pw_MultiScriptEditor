# coding=utf8

import os


def get_docs_content(file_name):
    cur_dir = os.path.dirname(__file__)
    _ = os.path.dirname(os.path.dirname(cur_dir))
    return os.path.join(_, "docs", file_name)
