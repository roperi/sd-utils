#!/usr/bin/env python3

import json
import sys
import os
import random
import argparse

def clean_filename(filename):
    return filename.split('_')[0]

def get_filenames_from_target_folders(input_folder, target_folder):
    target_folders = []
    for root, dirs, files in os.walk(input_folder):
        if target_folder in dirs:
            target_folders.append(os.path.join(root, target_folder))
    filename_list = []
    for path in target_folders:
        for root, dirs, files in os.walk(path):
            for filename in files:
                filename_list.append(clean_filename(filename))
    return filename_list


def main(filename, input_folder, target_folder, seed, samples, duplicate):
    """
    Create a XYZ prompt tests from caption filenames.

    Examples:
    $ python3 caption2prompt.py -d
    $ python3 caption2prompt.py -i input -t blip -S 15 --seed -1 -d
    $ wget -O - https://github.com/roperi/sd-utils/raw/main/caption2prompt.py | python3 - -d
    """
    caption_list = random.sample(get_filenames_from_target_folders(input_folder, target_folder), samples)

    # Extend caption list including captions without token
    caption_without_token = []
    if duplicate:
        for caption in caption_list:
            caption_without_token.append(caption.split(', ')[-1])

    prompt_list = caption_list + caption_without_token

    # Prepare data dict with captions as prompts
    data = []
    for prompt in prompt_list:
        d = {}
        d['prompt'] = prompt
        d['prompt_sr'] = '' 
        d['z_axis_type'] = 'Nothing'
        d['seed'] = seed
        data.append(d)

    # Save prompts to json file
    with open(filename, 'w') as fp:
        json.dump(data, fp)


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, default='xyz_prompt_tests.json', help='The name of the tests JSON file')
    parser.add_argument('-i', '--input_folder', type=str, default='input', help='The root folder where subfolders with caption filenames are located')
    parser.add_argument('-t', '--target_folder', type=str, default='blip', help='The name of the folder that contains caption filenames')
    parser.add_argument('--seed', type=int, default=555, help='Seed value')
    parser.add_argument('-S', '--samples', type=int, default=15, help='Number of filenames to generate')
    parser.add_argument('-d', '--duplicate', action="store_true", default=False, help='Duplicate every caption without its token (Def: True)')
    args = parser.parse_args()

    filename = args.filename
    input_folder = args.input_folder
    target_folder = args.target_folder 
    seed = args.seed 
    samples = args.samples 
    duplicate = args.duplicate

    # Run main
    main(filename, input_folder, target_folder, seed, samples, duplicate)

