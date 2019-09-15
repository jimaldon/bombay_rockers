DATASET_DIR=/home/amrit.krishnan/projects/bombay_rockers/data/tfrecords
CHECKPOINT_DIR="checkpoints"
CHECKPOINT_FILE=${CHECKPOINT_DIR}/model.ckpt-215197  # Example


CUDA_VISIBLE_DEVICES=1 python eval_image_classifier.py \
    --alsologtostderr \
    --checkpoint_path=${CHECKPOINT_FILE} \
    --dataset_dir=${DATASET_DIR} \
    --dataset_name=pc \
    --dataset_split_name=test \
    --model_name=mobilenet_v2 \
    --save_results=True
