########参数部分########
lr=1e-4
lora_rank=64
lora_alpha=128
lora_trainable="q_proj,v_proj,k_proj,o_proj,gate_proj,down_proj,up_proj"
modules_to_save="embed_tokens,lm_head"
lora_dropout=0.05

pretrained_model=/mnt/mydisk/llama2-merage-output/merge-llama2-chinese-alpaca-7B/V1/
chinese_tokenizer_path=/mnt/mydisk/llama2_models/chinese-alpaca-2-lora-7b
dataset_dir=/mnt/mydisk/LLaMA2-Alpaca2/data/train
per_device_train_batch_size=1
per_device_eval_batch_size=1
gradient_accumulation_steps=1
output_dir=/mnt/mydisk/llama2_sft_output
#peft_model=/mnt/mydisk/llama2_models/chinese-alpaca-2-lora-7b
validation_file=/mnt/mydisk/LLaMA2-Alpaca2/data/eval/alpaca_data_zh_51k.json
max_seq_length=1024

deepspeed_config_file=ds_zero2_no_offload.json

########启动命令########
torchrun --nnodes 1 --nproc_per_node 1 run_clm_sft_with_peft.py \
    --deepspeed ${deepspeed_config_file} \
    --model_name_or_path ${pretrained_model} \
    --tokenizer_name_or_path ${chinese_tokenizer_path} \
    --dataset_dir ${dataset_dir} \
    --validation_split_percentage 0.001 \
    --per_device_train_batch_size ${per_device_train_batch_size} \
    --per_device_eval_batch_size ${per_device_eval_batch_size} \
    --do_train \
    --do_eval \
    --seed $RANDOM \
    --fp16 \
    --num_train_epochs 2 \
    --lr_scheduler_type cosine \
    --learning_rate ${lr} \
    --warmup_ratio 0.03 \
    --weight_decay 0 \
    --logging_strategy steps \
    --logging_steps 10 \
    --save_strategy steps \
    --save_total_limit 3 \
    --evaluation_strategy steps \
    --eval_steps 250 \
    --save_steps 500 \
    --gradient_accumulation_steps ${gradient_accumulation_steps} \
    --preprocessing_num_workers 8 \
    --max_seq_length ${max_seq_length} \
    --output_dir ${output_dir} \
    --overwrite_output_dir \
    --ddp_timeout 30000 \
    --logging_first_step True \
    --torch_dtype float16 \
    --validation_file ${validation_file} \
    --gradient_checkpointing \
    --lora_rank ${lora_rank} \
    --lora_alpha ${lora_alpha} \
    --lora_dropout ${lora_dropout} \
    --trainable ${lora_trainable} \
    --modules_to_save ${modules_to_save} \
    --ddp_find_unused_parameters False


    #--peft_path ${peft_model} \

