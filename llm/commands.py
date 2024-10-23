"""
Original

python convert.py --torch-path <path_to_torch_model> --model-name tiny_llama

Generate with lora (without adapter) [DOES THIS WORK?]:
python3 llama.py --model-path /Users/daniel/Desktop/course-qa/llm/mlx-lora-model/config.json --prompt "Who is the 44th president of the USA?"
"""




"""

LORA
Quantize:
python convert.py --hf-path <hf_repo> -q

python3 convert.py --hf-path TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T --mlx-path /Users/daniel/Desktop/course-qa/llm/mlx-model -q 
4 bit quantisation

TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T



Generate (needs adapter):
python3 lora.py --model /Users/daniel/Desktop/course-qa/llm/mlx-lora-model --prompt "Who is the 44th president of the USA?"
"""