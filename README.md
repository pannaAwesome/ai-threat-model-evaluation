# Evaluation of AI-driven threat modelling tools
Repository with examples of threat models created by AI-driven threat modelling tools, and implementation of an evaluation method for judging the "correctness" of the models.

## Setup project on Ubuntu
1. Install virtual environment package on system `apt install python3.12-venv`
1. Create virtual environment `python3 -m venv threat_venv`
2. Activate the environment with `source threat_venv/bin/activate`
3. Install needed modules `pip3 install data-flow-diagram setuptools graphviz`
4. Install graphviz on system `apt install graphviz`

*The apt commands might need to be run with sudo*

## DFD 
It uses the *data-flow-diagram* module in python, the package and syntax is described here:
[DFD module](https://github.com/pbauermeister/dfd/blob/main/doc/README.md).

To render the dfd descriptions use  \
`data-flow-diagram [--output-file <OUTPUT-FILE-NAME>] [--format <gif,jpg,pdf>] <INPUT-FILE-NAME>`

The default command outputs the diagram as <INPUT-FILE-NAME>.svg, and it is possible to specify 
a different output file name and format, there are more formats than the ones listed above.
