from datetime import datetime
from os import walk
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import jinja2
import matplotlib.pyplot as plt
import numpy as np
import os

postfix = ['jpeg', 'jpg']

environment = jinja2.Environment()
template = environment.from_string("""---
weight: 1
images:
- /images/edited/{{number}}.jpeg
title: Picture
date: {{date}}
tags:
- luminar
- work
---
""")

def get_the_number(filname: str, image: bool = False):
    if image:
        return filname.split(".")[0]
    else:
        return filname.split(".")[0].split('-')[1]

def get_list_of_files(path: str, image: bool = False):
    f = set()
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            if file != "" and get_the_number(file, image) != "":
                f.add(get_the_number(file, image))
    return f

def get_date_taken(path):
    exif = Image.open(path)._getexif()
    if not exif:
        raise Exception('Image {0} does not have EXIF data.'.format(path))
    
    date_str = exif[36867]
    date_format = '%Y:%m:%d %H:%M:%S'
    return datetime.strptime(date_str, date_format)

def add_watermark(imagePath: str):
    # image opening
    image = Image.open(imagePath)
    draw = ImageDraw.Draw(image)
    exif = image.info['exif']
    w, h = image.size
    x, y = int(w / 2), int(h / 2)

    if x > y:
        font_size = y
    elif y > x:
        font_size = x
    else:
        font_size = x

    font = ImageFont.truetype("./static/fonts/YsabeauSC/YsabeauSC-Bold.ttf", int(font_size/12))

    draw.text((x, y), "German Alexis Rivera De La Torre Photos", fill=(255, 255, 255, 128), font=font, anchor='ms')
    image.save(imagePath, exif=exif)


# Get a list of pictures
# check if there is an image associated to a MD file
# if not find the next available number.
# rename the file to next number and create a file associated with it.
# Future Ideas - Check pictures
if __name__ == "__main__":
    image_path = "./assets/images/edited"
    md_path = "./content/work/edited"
    list_of_mds = get_list_of_files(md_path)
    list_of_pictures = get_list_of_files(image_path, image=True)
    diff_between = list_of_pictures - list_of_mds
    intersect_between = list_of_pictures.intersection(list_of_mds)
    highest_number_md = max([int(x) for x in list_of_mds])

    highest_number = len(intersect_between)

    print("List of MDs", len(list_of_mds))
    print("List of Intersect", len(intersect_between))

    print("Number of pictures", len(list_of_pictures))

    print("Difference", len(diff_between))
    print(list_of_pictures)

    for image in sorted(list_of_pictures):
        old_image_name = f"{image_path}/{image}.jpeg"
        md_file = f"{md_path}/edited-{image}.md"
        if os.path.isfile(old_image_name) and os.path.isfile(md_file):
            new_image_name = f"{image_path}/{highest_number}.jpeg"
            new_md_file = template.render(number=image, date=get_date_taken(new_image_name))
            with open(md_file, 'w') as f:
                f.write(new_md_file)
        else:
            highest_number = highest_number+1
            new_image_name = f"{image_path}/{highest_number}.jpeg"
            md_file = f"{md_path}/edited-{highest_number}.md"
            os.rename(old_image_name, new_image_name)
            new_md_file = template.render(number=highest_number, date=get_date_taken(new_image_name))
            with open(md_file, 'w') as f:
                f.write(new_md_file)
            