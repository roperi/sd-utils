#!/usr/env/bin python3

import os
import json
import webuiapi
import argparse

def main(filename, ckpt_folder, output_folder, sampler, steps, seed, cfg_scale, width, height):
    """
    Generate XYZ grids from a prompt test JSON file and save images and their respective text files to `output` folder.

    Examples:
    $ python3 generate_xyz_grids.py -f 'prompt_sr_tests.json' -C 'models/Stable-diffusion' -o 'output'
    $ python3 generate_xyz_grids.py -f 'xyz_prompt_tests.json'
    $ python3 generate_xyz_grids.py -f 'xyz_prompt_tests.json' -w 1024 -h 512
    $ wget -O - https://raw.githubusercontent.com/roperi/sd-utils/main/generate_xyz_grids.py | python3 - -f 'xyz_prompt_tests.json'
    """
    # Instantiate Webuiapi
    api = webuiapi.WebUIApi(host='127.0.0.1',
                        port=7860,
                        sampler=sampler,
                        steps=steps
                        )

    # Load checkpoints
    dir_name = ckpt_folder
    l = [name for name in os.listdir(dir_name) if name.endswith(".ckpt")]
    l.sort()
    # Shift last ckpt (sd1.5) to first item in list
    l = l[-1:] + l[:-1]
    checkpoints = ','.join(l)

    # Load prompts
    with open (filename, 'r') as j:
        prompt_tests_list = json.loads(j.read())

    # Create output folder
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    XYZPlotAvailableTxt2ImgScripts = [
    "Nothing",
    "Seed",
    "Var. seed",
    "Var. strength",
    "Steps",
    "Hires steps",
    "CFG Scale",
    "Prompt S/R",
    "Prompt order",
    "Sampler",
    "Checkpoint name",
    "Sigma Churn",
    "Sigma min",
    "Sigma max",
    "Sigma noise",
    "Eta",
    "Clip skip",
    "Denoising",
    "Hires upscaler",
    "VAE",
    "Styles",
    ]

    # Generate grid for each prompt test
    counter = 0
    for p in prompt_tests_list:
        counter += 1
        prompt = p.get('prompt')
        prompt_sr = p.get('prompt_sr')
        seed = str(p.get('seed'))
        z_axis_type = p.get('z_axis_type')
        # Prepare prompt
        XAxisType = "Seed"
        XAxisValues = seed 
        YAxisType = "Checkpoint name"
        YAxisValues = checkpoints
        ZAxisType = z_axis_type
        ZAxisValues = prompt_sr
        drawLegend = "True"
        includeLoneImages = "False"
        includeSubGrids = "False"
        noFixedSeeds = "False"
        marginSize = 0
        result = api.txt2img(
                    prompt=prompt,
                    seed=seed,
                    cfg_scale=cfg_scale,
                    width=width,
                    height=height,
                    script_name="X/Y/Z Plot",
                    script_args=[
                        XYZPlotAvailableTxt2ImgScripts.index(XAxisType),
                        XAxisValues,
                        XYZPlotAvailableTxt2ImgScripts.index(YAxisType),
                        YAxisValues,
                        XYZPlotAvailableTxt2ImgScripts.index(ZAxisType),
                        ZAxisValues,
                        drawLegend,
                        includeLoneImages,
                        includeSubGrids,
                        noFixedSeeds,
                        marginSize,                        ]
                    )
        seq = '{0:0>4}'.format(counter)
        path_filename = f'output/xyz_grid-{seq}-{seed}-{prompt}'
        result.image.save(f'{path_filename}.png')
        # Save txt file
        image_info =  f'''
        Prompt: {prompt}
        Steps: {steps}
        Sampler: {sampler}
        CFG scale: {cfg_scale}
        Script: X/Y/Z plot
        X Type: Seed
        X Values: {seed}
        Fixed X Values: {seed}
        Y Type: Checkpoint name
        Y Values: {checkpoints}
        Z Type: {z_axis_type}
        Z Values: "{prompt_sr}"
        '''
        with open(f"{path_filename}.txt", "w") as f:
            f.write(image_info)


if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, default='prompt_tests.json', help='The name of the tests JSON file')
    parser.add_argument('-C', '--ckpt_folder', type=str, default='models/Stable-diffusion/', help='Folder where ckpts are located')
    parser.add_argument('-o', '--output_folder', type=str, default='output', help='Folder where images and text files will be saved to')
    parser.add_argument('-S', '--sampler', type=str, default='Euler a', help='Sampler')
    parser.add_argument('-t', '--steps', type=int, default=20, help='Steps value')
    parser.add_argument('-s', '--seed', type=int, default=555, help='Seed value')
    parser.add_argument('-c', '--cfg_scale', type=float, default=7.0, help='CFG value')
    parser.add_argument('-W', '--width', type=int, default=512, help='Width value')
    parser.add_argument('-H', '--height', type=int, default=512, help='Height value')
    args = parser.parse_args()

    filename = args.filename
    ckpt_folder = args.ckpt_folder
    output_folder = args.output_folder
    sampler = args.sampler
    steps = args.steps
    seed = args.seed
    cfg_scale = args.cfg_scale
    width = args.width
    height = args.height

    # Run main
    main(filename, ckpt_folder, output_folder, sampler, steps, seed, cfg_scale, width, height)
