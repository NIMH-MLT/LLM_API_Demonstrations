# LLM_API_Demonstrations

This repository contains demonstration functions for carrying various tasks with LLMs using the API, against different backends (Ollama, with either native or OpenAI APIs, and Hugging Face)

## Ollama

To use, first create a conda environment

	conda create --name ollama

and install the ollama API

	pip install ollama


### demo_ollama_chat.py

This is a demo for interaction with an LLM (single turn, or chat). 

### demo_ollama_images.py

This is a demo for passing images to a VLM, asking it to do tasks, and outputting structured JSON (for the triplet task).


## Hugging Face

### demo_huggingface_local_model.py

This demo loads a model from the local `../models/` folder (Qwen3.5-0.8B by default) and runs inference locally via the Hugging Face `transformers` library. The conversation pattern is identical to `demo_ollama_backend.py`; only the inference call changes.

Create a fresh conda environment in this folder:

	conda create --prefix ../envs/hf-local python=3.11
	conda activate ../envs/hf-local

and install the dependencies:

	pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
	pip install transformers accelerate pillow safetensors

(the explicit `--index-url` pins torch to a CUDA 12.4 build, which is what works on our hardware; on a different machine you may want a different CUDA build or the CPU-only one).
