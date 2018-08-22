# coding=utf8

import os


def get_image_path(image_name):
    cur_dir = os.path.dirname(__file__)
    _ = os.path.dirname(os.path.dirname(cur_dir))
    images_folder = os.path.join(_, "images")

    images = dict(
        pw=os.path.join(images_folder, 'pw.png'),
        all=os.path.join(images_folder, 'exec_all.png'),
        sel=os.path.join(images_folder, 'exec_sel.png'),
        clear=os.path.join(images_folder, 'clear.png'),
        help=os.path.join(images_folder, 'help.png'),
        donate=os.path.join(images_folder, 'donate.png'),
    )
    return images.get(image_name)
