# Demos for using Jev and Jev-like models

The code runs in a python environment, where the only thing you'll need to install is `requests`.

## Jev

Jev is only available in the cloud, so an OpenRouter key is needed. I'll assume that is stored in the environment variable OPENROUTER_API_KEY for this section of the demo. I'm following instructions from 

https://openrouter.ai/docs/guides/community/jev-tutorial

## clef-flash, clef, and nimble

These are available through the Ollama backend in all our servers, and are easy to install in your laptop after installing Ollama, with

	ollama pull clef-flash
	ollama pull clef
	ollama pull nimble
	
## running the code

The function to run is `demo_jev_and_clef.py`, which demonstrates all three types of query supported by Jev and the other models. The code has switch for model choice, and the rest is automatically determined from that. Note that Jev requires setting `verify=False` line at the beginning, which is needed if running this at NIH or on the VPN, unless you know how to work around this by keeping a local copy of the NIH HTTPS certificate.


