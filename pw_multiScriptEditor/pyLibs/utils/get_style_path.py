# coding=utf8

import os


def get_style_path(style_name):
    cur_dir = os.path.dirname(__file__)
    _ = os.path.dirname(os.path.dirname(cur_dir))
    return os.path.join(_, "style", style_name)
