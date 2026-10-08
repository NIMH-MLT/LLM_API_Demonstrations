# Running Claude Code with an open-weight model on Biowulf

For questions about this guide, please contact the NIMH Machine Learning Core (NIMHMLC@mail.nih.gov).
    
## what is this, and what is it for?

Mainly, to allow you to use the Claude Code development environment when you cannot buy a subscription for it from Anthropic, due to cost or purchasing constraints.

The Claude Code access one buys is a combination of a "harness" (code running on your machine or browser, which you interact with) and Opus, a large language model (LLM) provided by Anthropic (running on their servers, the harness talks to this LLM to provide tasks, or collect results). What this guide shows is how to substitute the LLM for an open-weight LLM (from any provider), running on Biowulf GPUs (for free), served through a local back-end called Ollama. While these open-weight LLMs are not quite as smart as Opus, they are very good at programming, the key reason for using Claude Code, and across many other tasks.
        

    
## preparation

Install Claude Code (it will force install into $HOME/.claude. but it doesn't take much space)

    curl -fsSL https://claude.ai/install.sh | bash

    
Create a folder for running it in,

    mkdir Test_CC

If you are interested in having it work on code in github, you can also clone the relevant repository and use that as the folder.

    
## start an interactive session with access to a GPU

For this demo, we will use a L40 GPU (with 48GB of RAM in the card)

     sinteractive --mem=32g --gres=gpu:l40:1

This may take a bit of time to schedule, since this GPU model is in high demand. LLMs are sized in terms of billions of parameters, and this GPU handles (almost) every model we have in the Ollama back-end. We will discuss choice of model and GPU later in this document.


## set it up

Run the following commands to set up CUDA (NVIDIA's software to access GPU cards), and start the Ollama back-end

    module load CUDA/12.8.2
    module load ollama
    export OLLAMA_MODELS=/data/NIMH_ReadOnly/Ollama_models
    export OLLAMA_CONTEXT_LENGTH=256000
    `ollama_start | grep export`
    
Paste that into the command line (notice the backticks in the last line), and now check that it all works

    echo $OLLAMA_MODELS
    echo $OLLAMA_HOST

should give you (the number in localhost:<number> will vary)

    /data/NIMH_ReadOnly/Ollama_models
    localhost:22919

and

    ollama ls

will show you all the models available. If no models show, something is wrong. If the model you want is not in there, it can be installed. Either way, please let us know!

If, at any point, you get the error message

    Error: could not connect to ollama server, run 'ollama serve' to start it

then just redo

    `ollama_start | grep export`

and try

    ollama ls

again.
    
## run a model

Try running a small model, which should load quickly

    ollama run qwen3.5:9b 

If successful, you will get a prompt you can interact with, e.g. type

    >>> why is the sky blue?

and you'll see the thinking trace from the model as it tries to solve the problem.

This shows us that Ollama can run a model, and Claude Code can rely on it.


## run Claude Code

Set a few more environment variables, which point Claude Code to the Ollama back-end
    
    export ANTHROPIC_AUTH_TOKEN=ollama
    export ANTHROPIC_BASE_URL=$OLLAMA_HOST
    export ANTHROPIC_API_KEY=""
    export CLAUDE_CODE_MAX_CONTEXT_TOKENS=$OLLAMA_CONTEXT_LENGTH
            
and then go into the folder you set aside for Claude Code, and start it with a coding model

    cd Test_CC
    claude --model qwen3-coder:30b

It will ask you if you trust the folder, so use the cursor keys to select yes and enter.

At this point, you can provide it with instructions, e.g.

    write me a python function to compute the first k prime numbers

and it will do. At that point, you can ask it to change the function, write it to a file, or anything else you would do with a coding assistant. That's it, you're using Claude Code!

## improving performance and using other models

Models come in a variety of sizes, quantified by #parameters. In general, the more parameters, the higher the capability, and the slower the model runs. For the purpose of running Claude Code, `qwen3-coder:30b` is a good compromise. For other purposes, the best approach is to find a model that works well, and then work downwards in number of parameters tofind one that still does the task. The Ollama back-end makes it easy to see what that number is for a given model, as the models are usually named `<model>:<#parameters>-<features>`. 

The other consideration is which GPU to run on, which depends on the RAM capacity needed (the bigger the model, the more RAM is needed), and the speed. The short answer is: l40, which is a good trade-off and can fit almost any relevant models. To go further, this table shows which models fit on each Biowulf GPU type:

|GPU <BR> model (parameters)| context | v100 |v100x| l40 | a100|
|---------------------|----- |-----|-----|-----|-----|
|qwen3.5:9b           | 256K |  x  |  x  |  x  |  x  |
|qwen3-coder:30b      | 256K |     |  x  |  x  |  x  |
|qwen3.8 (27b)        | 256K |     |  x  |  x  |  x  |
|gemma4:12b-it-qat    | 256K |  x  |  x  |  x  |  x  |
|gemma4:26b-a4b-it-qat| 256K |     |  x  |  x  |  x  |
|gpt-oss:20b          | 128K |     |  x  |  x  |  x  |
|gpt-oss:120b         | 128K |     |     |  x  |  x  |
|mistral-medium-3.5   | 256K |     |     |     |  x  |

This table shows how much memory each model has, and how fast they are (comparatively)
    
| GPU  | memory | speed |
|------|--------|-------|
|v100  | 16GB   | 1     |
|v100x | 32GB   | 1     |
|a100  | 80GB   | 2     |
|l40   | 48GB   | 3     |
|h200  | 141GB  | 4     |

The H200 is the most capable GPU, but also the least likely to be available for interactive use, and it would be wasteful to use it for a model that would fit in smaller GPUs. In general, you should use the smallest GPU that the model will run in, and where the speed is acceptable, for ease of scheduling.

## other resources

If you want to get a better handle on how to effectively use Claude Code, this book chapter by Russ Poldrack is a great starting point

    https://bettercodebetterscience.github.io/book/ai-coding-assistants/

## Application Programming Interface (API) use

It is possible to support your python programs interacting with the models running on the Ollama back-end, using an application programming interface (API). We are writing a guide about this, with samples, so if you would be interested in doing that please contact the NIMH Machine Learning Core (NIMHMLC@mail.nih.gov).
