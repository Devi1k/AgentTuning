docker run --gpus all -it \
  --shm-size 16g \
  -v /mnt/d/ft:/data \
  110853232732 \
  bash








swift sft \
  --model /data/Qwen3-4B-Instruct-2507 \
  --train_type qlora \
  --dataset /data/AgentTuning/val_set_200.json \
  --max_length 1024 \
  --per_device_train_batch_size 1 \
  --gradient_accumulation_steps 8 \
  --learning_rate 2e-4 \
  --max_steps 20 \
  --logging_steps 1 \
  --save_steps 20 \
  --bf16 true \
  --gradient_checkpointing true \
  --loss_scale last_round \
  --output_dir /data/mvp_qwen3_4b_qlora_last_round
