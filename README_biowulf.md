# LLM_API_Demonstrations

This repository contains demonstration functions for carrying various tasks with LLMs using the API, against different backends (Ollama, with either native or OpenAI APIs, and Hugging Face)


## demo_huggingface_local_model.py

This demo loads a model from the local NIMH model repo on biowulf and runs inference locally via the Hugging Face `transformers` library. The conversation pattern is identical to `demo_ollama_backend.py`; only the inference call changes.

Create a fresh conda environment and activate it:

    conda create --name demo_huggingface python=3.12
	conda activate demo_huggingface

and install the dependencies:

    module load CUDA/12.8.1
	pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
	pip install transformers accelerate pillow safetensors

(CUDA 12.8.1 is the latest available, the explicit `--index-url` pins torch to a CUDA 12.6 build, which is the closest pytorch match)

## (NOT UPDATED FOR BIOWULF YET)
## demo_ollama_backend.py

To use, first create a conda environment

	conda create --name ollama

and install the ollama API

	pip install ollama

and, optionally, the OpenAI API
(f you want to use that component of the demo)

	pip install openai
