# LLM_API_Demonstrations

This repository contains demonstration functions for carrying various tasks with LLMs using the API, against different backends (Ollama, with either native or OpenAI APIs, and HuggingFace)

## setup conda environment for HuggingFace

This is needed for running every HuggingFace demo. If you do not yet have miniconda set up, follow the instructions in

https://hpc.nih.gov/docs/diy_installation/conda.html

You can also use other software for creating virtual environments. If using conda, these are the commands to create a fresh environment and activate it

    conda create --name demo_huggingface python=3.12
	conda activate demo_huggingface

Once you have an environment active, you need to install the following packages

    module load CUDA/12.8.1
	pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
	pip install transformers accelerate pillow safetensors

(CUDA 12.8.1 is the latest available, the explicit `--index-url` pins torch to a CUDA 12.6 build, which is the closest pytorch match)
If all finishes without errors, you are done with setting up the enviroment.

    
## verify that everything works

We can verify that this demo (or any other code you write) works by setting up an interactive session with a GPU
    
    sinteractive --mem=32g --gres=gpu:a100:1

and then activating the environment

    conda activate demo_huggingface

and running the interactive chat demo

    python demo_biowulf_huggingface_chat.py 

This loads an LLM from the NIMH repository at

    /data/NIMH_ReadOnly/HF_models/

and sets up a chat. The first question is prompted for you, namely

    "Why is the sky blue?"

and the LLM will provide a response. Then you will get another prompt

    "user says:"

and you can type further, or simply press enter at an empty prompt to stop writing.
    
 
## use the model in batch mode

Now that we checked that everything works for the chat, let's try running a script that can do an arbitrary task using the LLM. This code just takes a prompt, and outputs a response

    python demo_biowulf_huggingface_script.py

In this case, the prompt is still "Why is the sky blue?", and you will get a response to that with no constraints on length. You can exit the interactive session now.


## run model from biowulf command line

Finally, let's run the script from the biowulf command line, using swarm.

The demo includes a sample demo.submit file, which you should edit to replace

    /data/pereiraf2/LLM_API_Demonstrations/demo_biowulf_huggingface_script.py

with the path to your copy of this file. After you do that, activate the environment (all jobs will inherit this)

    conda activate demo_huggingface

and submit this swarm command line

    swarm --module CUDA/12.8.1 --gb-per-process 16 --time 04:00:00  --partition gpu --gres=gpu:a100:1 --qos=gpunimh2025.1 demo.submit

noting the job ID number submitted. You can use

    jobhist <job ID>

to keep track, and see if COMPLETED or FAILED. Once it finishes, there should be a file

    demo_script_output.txt

with the output of running for this prompt. It will also output

    swarm_<job ID>.o (commands executed)
    swarm_<job ID>.e (any warnings or errors, if the job failed)

    
    
## (NOT UPDATED FOR BIOWULF YET)
## demo_ollama_backend.py

To use, first create a conda environment

	conda create --name ollama

and install the ollama API

	pip install ollama

and, optionally, the OpenAI API
(f you want to use that component of the demo)

	pip install openai
