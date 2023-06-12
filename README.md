![grid of parts](docs/parts.png)

# Lego Rendering Pipeline

Render semi-realistic, individual parts. Primarily used to train
machine learning models for detection, part classification and color
classification.

This uses LDraw's part models and Blender to produce a render.

A single render typically takes 10-15s on an M1 Pro. There is a draft mode
that takes a few seconds.


## Sample

```python
renderer = Renderer(ldraw_path="./ldraw")

renderer.render_part("6126b", RenderOptions(
    image_filename = "renders/test.jpg",
    part_color = RebrickableColors.Blue.value.best_hex,
    material = Material.PLASTIC,
    lighting_style = LightingStyle.BRIGHT,
    light_angle = 160,
    part_rotation = (0, 0, 270),
    camera_height = 45,
    zoom = 0.1,
    look = Look.NORMAL,
    render_width = 244,
    render_height = 244,
))

```
See `lib/renderer/render_options.py` for the full list of options. See `docs-*.py` to see how the images on this page were genereated.

## Parts

In theory this can render any LDraw part. However I've only tested with typical plastic Lego parts. Parts are specified using their LDraw ID. In many cases this will be same as the mold number on the part but not always. Keep in mind there may be multiple molds over time.


## Materials

Currently supports plastic, transparent and rubber. Not supported yet: glitter, pearlescent, glitter, glitter, metal and cloth.

![grid of materials](docs/materials.png)


## Colors

Ccolors are specified with hex codes in sRGB. Included is a list of named colors from Rebrickable.


![grid of colors](docs/colors.png)


## Rotation

Parts can be rotated to various angles. The parts are moved up/down to
remain touching the ground.

![grid of various rotations](docs/part_rotations.png)


## Lighting

Lighting Styles: default, bright, hard

![grid of lighting styles](docs/lighting_styles.png)

Lighting angle around the part

![grid of light angles](docs/light_angles.png)


## Camera

Camera height: degrees from 0-90

![grid of various camera angles](docs/camera-heights.png)

Camera zoom

![grid of various zoom levels](docs/zooms.png)


## Special Parts

Various parts that have caused trouble. Partially here so I know they continue to work.
* Slopes: have a textured material on the slope
* Multi-part / multi-mesh parts
* Patterns

![grid of special parts](docs/special.png)


## Instruction Look

![grid of various parts in line art style](docs/instructions.png)


## Setup

- Install [Blender](https://blender.org)
- Download [ImportLDraw Plugin](https://github.com/TobyLobster/ImportLDraw)
- [LDraw parts library](https://library.ldraw.org/updates?latest)
  - download the complete zip
  - extract into ./ldraw, e.g. ./ldraw/parts/30010.dat
- [LDraw unofficial parts](https://library.ldraw.org/tracker)
  - download all Unofficial Files
  - extract into ./ldraw/unofficial, e.g. ./ldraw/unofficial/parts/22388.dat
- Run
    ```
    ./setup.sh
    ```

## Run

We need to run in Blender's Python environment:

```
./run.sh test.py         # renders to renders/test/png

./run-watch.sh test.py   # run test.py each time a .py file is saved
```
