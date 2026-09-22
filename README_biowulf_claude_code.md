# Running Claude Code with an open-weight model on Biowulf

These instructions are for running Claude Code (an agentic coding harness) on an open-weight LLM (not from Anthropic) on Biowulf GPUs, served by the Ollama back-end. The primary reason for doing this would not being able to get access to Claude Code using Anthropic's LLMs, because of subscription price, or purchasing constraints.

For questions about this guide, please contact the NIMH Machine Learning Core (NIMHMLC@mail.nih.gov).
    
## preparation

Install Claude Code (it will force install into $HOME/.claude. but it doesn't take much space)

    curl -fsSL https://claude.ai/install.sh | bash

    
Create a folder for running it in,

    mkdir Test_CC

If you are interested in having it work on code in github, you can also clone the relevant repository and use that as the folder.

    
## start an interactive session with access to a GPU

For this demo, we will use a medium GPU (v100x, 32GB of RAM)

    sinteractive --mem=32g --gres=gpu:v100x:1

which can schedule quickly, and run smaller models. Models are sized in terms of billions of parameters, and this should handle anything up to ~20B parameters. For larger models, or faster performance, the only option is the larger GPUs (A100, 80GB of RAM)

    sinteractive --mem=32g --gres=gpu:a100:1

but those are heavily subscribed, at least until the next GPU upgrade.
    
    
## set it up

Run the following commands to set up CUDA (NVIDIA's software to access GPU cards), and start the Ollama back-end

    module load CUDA/12.8.2
    export OLLAMA_MODELS=/data/NIMH_ReadOnly/Ollama_models
    module load ollama
    ollama_start

The last line starts the back-end, and gives you a line that looks like this (the :<number> might vary)

    export OLLAMA_HOST=localhost:22919

Paste that into the command line, and now check that it all works

    echo $OLLAMA_MODELS
    echo $OLLAMA_HOST

should give you

    /data/NIMH_ReadOnly/Ollama_models
    localhost:22919

and

    ollama ls

will show you all the models available. If the one you want is not in there, let us know.

    
## run a model

Try

    ollama run qwen3.5:9b

If successful, you will get a prompt you can interact with, e.g. type

    >>> why is the sky blue?

and you'll see the thinking trace from the model as it tries to solve the problem.

This shows us that Ollama can run a model, and Claude Code can rely on it.


## run Claude Code

Set a few more environment variables
    
    export ANTHROPIC_AUTH_TOKEN=ollama
    export ANTHROPIC_BASE_URL=$OLLAMA_HOST
    export ANTHROPIC_API_KEY=""
    export OLLAMA_CONTEXT_LENGTH=256000
    
and then go into the folder you set aside for Claude Code, and start it

    cd Test_CC
    claude --model qwen3.5:9b

It will ask you if you trust the folder, so use the cursor keys to select yes and enter.

At this point, you can provide it with instructions, e.g.

    write me a python function to compute the first k prime numbers

and it will do so (possibly a bit slowly, with this GPU). At that point, you can ask it to change the function, write it to a file, or anything else you would do with a coding assistant. That's it, you're using Claude Code!


## improving performance

    
TODO: wait for new GPUs to come online


## other resources

If you want to get a better handle on how to effectively use Claude Code, this book chapter by Russ Poldrack is a great starting point

    https://bettercodebetterscience.github.io/book/ai-coding-assistants/

