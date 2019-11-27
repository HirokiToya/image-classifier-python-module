import glob
import os
import re
import json
import random
import shutil


def read_json_file(file_path):
    f = open(file_path, 'r')
    return json.load(f)


def rand_ints_nodup(range_from, range_to, count):
    ns = []
    while len(ns) < count:
        n = random.randint(range_from, range_to)
        if n not in ns:
            ns.append(n)

    return ns


if __name__ == '__main__':

    json_data = read_json_file("input/data/image_name.json")
    all_images_path = glob.glob("./input/images_8000/*.jpg")
    from_dir = "./input/images_8000"
    to_dir = "./output/images_400"

    for key in json_data.keys():

        random_indexes = rand_ints_nodup(1, 200, 10)
        target_images = [os.path.basename(img_path) for img_path in all_images_path if key in os.path.basename(img_path)]

        for image in target_images:

            num = re.sub("\\D", "", image)

            if int(num) not in random_indexes:
                continue

            image_path = from_dir+"/"+image
            dst_path = os.path.join(to_dir, image)
            shutil.copy(image_path, dst_path)
            print('move: {} -> {}'.format(image, dst_path))