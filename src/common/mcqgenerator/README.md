# README



pip install -e .

simple application with Langcahin, 
it uses SequentialChain to chain to prompts: the output of the first chain is used as input of the second.
I use also get_openai_callback to track the token usage in Langchain.

## subjects of this project
* Template prompts: selector by length: https://python.langchain.com/docs/modules/model_io/prompts/example_selectors/length_based/
* Sequential chains, Chain where the outputs of one chain feed directly into next: https://api.python.langchain.com/en/latest/chains/langchain.chains.sequential.SequentialChain.html
* Multiple chains: https://python.langchain.com/docs/expression_language/cookbook/multiple_chains/

