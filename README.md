# Gcode-splicer
A script to splice multiple 3D printer gcode files together.

## Description
This script outputs a gocde file with an equal number of layers taken from each of the input files. You can also specify a layer to begin the equal split from. Layers are added in equally sized sections taken from the input files in the order they are give. All lines before the first (or specified) layer are taken from the first input file and all lines after the last layer are taken from the last input file.

The input gcode files must contain an equal number of files, and should contain code sliced from the same 3D model. If different models are used in each input file this script makes no effort to line them up.

This script is intended to be used for creating calibration prints. This is done by slicing the same model multiple times, modifying a single settings value each time. Once the output gcode is printed you will be able to determine the best value for that setting from the most desirable section of the objects height.

## Usage

`gcode_splicer.py` takes the following arguments along with a list of input files

* `-o` `--output-file`: The filename to use for the output file.

* `-s` `--start-layer`: The number of the layer to start from. Optional.
