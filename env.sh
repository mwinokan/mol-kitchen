#!/bin/bash

conda create --name mace python=3.9
conda activate mace
pip install torch torchvision torchaudio
pip install mace-torch
pip install mpytools typer IPython molparse pre-commit black
