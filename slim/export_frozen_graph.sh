CUDA_VISIBLE_DEVICES=1 python3 tensorflow/python/tools/freeze_graph.py \
  --input_graph=../bombay_rockers/slim/train_logs/mobilenet_pc.pb \
  --input_checkpoint=../bombay_rockers/slim/checkpoints/model.ckpt-474932 \
  --input_binary=true --output_graph=../bombay_rockers/slim/train_logs/mobilenet_pc_fg.pb \
  --output_node_names=MobilenetV2/Predictions/Reshape_1
