# Evaluation of AI-driven threat modelling tools

Repository with examples of threat models created by AI-driven threat modelling tools, and implementation of an evaluation method for judging the "correctness" of the models.

## Setup project on Ubuntu

1. Install virtual environment package on system `apt install python3.12-venv`
2. Create virtual environment `python3 -m venv threat_venv`
3. Activate the environment with `source threat_venv/bin/activate`
4. Install needed modules `pip3 install data-flow-diagram setuptools graphviz`
5. Install graphviz on system `apt install graphviz`

*The apt commands might need to be run with sudo*

### LLM API
The LLM setup uses openAI and it is compatible with any provider that supports this format. Examples would be:
- OpenRouter
- Ollama
- OpenAI
- and many more

For any provider you will need to setup a .env file containing your api key and api endpoint, the file should contain
the following:
```
OPENAI_API_KEY=<your-api-key>
OPENAI_ENDPOINT=<api-endpoint-to-target>
```
> *For local providers you can set the api key to a dummy value*

**Ollama Setup:** \
You install Ollama by running `curl -fsSL https://ollama.com/install.sh | sh`

After this you can run the entire project through the `run_all_experiments.sh` file, or you can pull selected models and run the `judge_threat_models.py` with your pulled model. For the project, you can find som suggested models based on your system strength in *ollama/models_to_use.txt*.

## DFD

It uses the *data-flow-diagram* module in python, the package and syntax is described here:
[DFD module](https://github.com/pbauermeister/dfd/blob/main/doc/README.md).

To render the dfd descriptions use  \
`data-flow-diagram [--output-file <OUTPUT-FILE-NAME>] [--format <gif,jpg,pdf>] <INPUT-FILE-NAME>`

The default command outputs the diagram as <INPUT-FILE-NAME>.svg, and it is possible to specify
a different output file name and format, there are more formats than the ones listed above.
