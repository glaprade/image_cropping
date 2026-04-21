#!/bin/bash
#SBATCH --job-name=cropping
#SBATCH --output=analysis_output.txt
#SBATCH --error=analysis_error.txt
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=4


source /home/glapr/projects/def-cbrown/glapr/ImagePreprocessing/processing_venv/bin/activate

python image_preprocessing.py