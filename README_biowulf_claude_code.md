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

For this demo, we will use a large GPU (A100, 80GB of RAM)

     sinteractive --mem=32g --gres=gpu:a100:1

Models are sized in terms of billions of parameters, and this should handle every model we have in the Ollama back-end. For smaller models (up to ~30B parameters), it's possible to use a medium GPU (v100x, 32GB of RAM)

    sinteractive --mem=32g --gres=gpu:v100x:1

which can be scheduled in an interactive session almost instantly.

Models served in the Ollama back-end are usually named `<model>:<#parameters>-<features>`. In general, you should use the smallest GPU that the model will run in, with the following table showing which models will run in which GPUs available now (v100:16GB, v100x:32GB, A100:80GB).

|model (parameters)|context length| v100 |v100x|a100 |
|-----------------|-----|-----|-----|-----|
|qwen3.5:9b       | 256K |  x  |  x  |  x  |
|qwen3-coder:30b  | 256K |     |  x  |  x  |     
|qwen3.8 (27b)    | 256K |     |  x  |  x  |
|gemma4:12b-it-qat| 256K |  x  |  x  |  x  |
|gemma4:26b-a4b-it-qat| 256K |     |  x  |  x  |
|gpt-oss:20b      | 128K |     |  x  |  x  |
|gpt-oss:120b     | 128K |     |     |  x  |

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
    export CLAUDE_CODE_MAX_CONTEXT_TOKENS=$OLLAMA_CONTEXT_LENGTH
            
and then go into the folder you set aside for Claude Code, and start it with a coding model

    cd Test_CC
    claude --model qwen3-coder:30b

It will ask you if you trust the folder, so use the cursor keys to select yes and enter.

At this point, you can provide it with instructions, e.g.

    write me a python function to compute the first k prime numbers

and it will do so (possibly a bit slowly, with this GPU). At that point, you can ask it to change the function, write it to a file, or anything else you would do with a coding assistant. That's it, you're using Claude Code!


## improving performance

    
TODO: wait for new GPUs to come online


## other resources

If you want to get a better handle on how to effectively use Claude Code, this book chapter by Russ Poldrack is a great starting point

    https://bettercodebetterscience.github.io/book/ai-coding-assistants/

