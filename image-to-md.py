from os import walk
import os
import jinja2
import datetime
from PIL import Image

postfix = ['jpeg', 'jpg']

environment = jinja2.Environment()
template = environment.from_string("""
---
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
            f.add(get_the_number(file, image))
    return f

def get_date_taken(path):
    exif = Image.open(path)._getexif()
    if not exif:
        raise Exception('Image {0} does not have EXIF data.'.format(path))
    return exif[36867]


if __name__ == "__main__":
    image_path = "./assets/images/edited"
    md_path = "./content/work/edited"
    list_of_mds = get_list_of_files(md_path)
    list_of_pictures = get_list_of_files(image_path, image=True)
    new_list_of_pictures = list_of_pictures - list_of_mds
    highest_number = max([int(x) for x in list_of_mds])
    print(highest_number, new_list_of_pictures )
    for image in sorted(new_list_of_pictures):
        print(image)
        if os.path.isfile(f"{image_path}/{image}.jpg"):
            highest_number = highest_number+1
            print(image, highest_number)
            old_image_name = f"{image_path}/{image}.jpg"
            new_image_name = f"{image_path}/{highest_number}.jpg"
            new_md_file = template.render(number=highest_number, date=get_date_taken(old_image_name))
            print(template.render(number=highest_number, date=datetime.datetime.now()))
            with open(f"{md_path}/edited-{highest_number}.md", 'w') as f:
                f.write(new_md_file)
            os.rename(old_image_name, new_image_name)


    # Get a list of pictures
    # check if there is an image associated to a MD file
    # if not find the next available number.
    # rename the file to next number and create a file associated with it.


    # Future Ideas - Check pictures