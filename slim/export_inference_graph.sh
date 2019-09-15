CUDA_VISIBLE_DEVICES=1 python3 export_inference_graph.py \
  --alsologtostderr \
  --model_name=mobilenet_v2 \
  --image_size=256 \
  --output_file=train_logs/mobilenet_pc.pb \
  --dataset_name=pc
