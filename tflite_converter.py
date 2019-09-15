import tensorflow as tf
import sys

converter = tf.lite.TFLiteConverter.from_frozen_graph(sys.argv[1], input_arrays=["input"], output_arrays=["MobilenetV2/Predictions/Reshape_1"])
tflite_model = converter.convert()
out = sys.argv[2]+"/"+"converted_model.tflite"
open(out, "wb").write(tflite_model)
