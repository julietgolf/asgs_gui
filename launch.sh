#!/bin/bash
module load apptainer
exec apptainer shell --fakeroot --writable --bind ~/container_files/containers/asgs/gui/adcirc:/opt/asgs/opt/models/adcircs  asgs_gui

