from os import walk
import os
import jinja2
import datetime
from PIL import Image
from datetime import datetime

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
            f.add(get_the_number(file, image))
    return f

def get_date_taken(path):
    exif = Image.open(path)._getexif()
    if not exif:
        raise Exception('Image {0} does not have EXIF data.'.format(path))
    
    date_str = exif[36867]
    date_format = '%Y:%m:%d %H:%M:%S'
    return datetime.strptime(date_str, date_format)


if __name__ == "__main__":
    image_path = "./assets/images/edited"
    md_path = "./content/work/edited"
    list_of_mds = get_list_of_files(md_path)
    list_of_pictures = get_list_of_files(image_path, image=True)
    new_list_of_pictures = list_of_pictures - list_of_mds
    highest_number = max([int(x) for x in list_of_mds])
    print(new_list_of_pictures)
    for image in sorted(list_of_pictures):
        if os.path.isfile(f"{image_path}/{image}.jpeg"):
            highest_number = highest_number+1
            old_image_name = f"{image_path}/{image}.jpeg"
            # new_image_name = f"{image_path}/{highest_number}.jpeg"
            new_md_file = template.render(number=image, date=get_date_taken(old_image_name))
            print(image, old_image_name)
            with open(f"{md_path}/edited-{image}.md", 'w') as f:
                f.write(new_md_file)
            # os.rename(old_image_name, new_image_name)


    # Get a list of pictures
    # check if there is an image associated to a MD file
    # if not find the next available number.
    # rename the file to next number and create a file associated with it.


    # Future Ideas - Check pictures