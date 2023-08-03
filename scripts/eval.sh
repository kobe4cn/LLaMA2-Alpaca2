model_path=/mnt/mydisk/llama2-merage-output/merge-llama2-chinese-alpaca-7B/V2
output_path=/mnt/mydisk/llama2-merage-output/merge-llama2-chinese-alpaca-7B/ceval/

cd scripts/ceval
python eval.py \
    --model_path ${model_path} \
    --cot False \
    --few_shot False \
    --with_prompt True \
    --constrained_decoding True \
    --temperature 0.2 \
    --n_times 1 \
    --ntrain 5 \
    --do_save_csv False \
    --do_test False \
    --output_dir ${output_path}