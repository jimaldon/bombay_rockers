from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from os.path import join
import sys
import contextlib2

import numpy as np
import cv2
from six.moves import cPickle
from six.moves import urllib
import tensorflow as tf

import dataset_utils


_NUM_TRAIN_FILES = 4


def _create_tfrecord(dataset_dir, tfrecord_writer, classes_train):
	count = 0
	for cls_train in classes_train:
		image_names = list(filter(lambda x: x.endswith('JPG') or x.endswith('jpg'), os.listdir(join(dataset_dir, 'train', cls_train))))
		num_images =  len(image_names)
		for i, im_name in enumerate(image_names):
			im_path = join(dataset_dir, 'train', cls_train, im_name)
			with tf.gfile.Open(im_path, 'rb') as f:
				img = cv2.imread(im_path)
				_, encoded_image = cv2.imencode('.jpg', img)
				label = classes_train[cls_train]
				encoded_image = encoded_image.tobytes()
				example = dataset_utils.image_to_tfexample(
            		encoded_image, b'jpg', 256, 256, label)

				output_shard_index = count % _NUM_TRAIN_FILES
				tfrecord_writer[output_shard_index].write(example.SerializeToString())
				count += 1
				print('Processed {} images'.format(count))


def _get_output_filename(dataset_dir, split_name):
  """Creates the output filename.
  Args:
	dataset_dir: The dataset directory where the dataset is stored.
	split_name: The name of the train/test split.
  Returns:
	An absolute file path.
  """
  return '%s/pc_dataset_%s.tfrecord' % (dataset_dir, split_name)


def run(dataset_dir):
  """Runs the download and conversion operation.
  Args:
	dataset_dir: The dataset directory where the dataset is stored.
  """
  if not tf.gfile.Exists(dataset_dir):
	  tf.gfile.MakeDirs(dataset_dir)

  training_filename = _get_output_filename(dataset_dir, 'train')
  # testing_filename = _get_output_filename(dataset_dir, 'test')
  
  classes_train = sorted(list(filter(lambda x: os.path.isdir(join(dataset_dir, 'train', x)), os.listdir(join(dataset_dir, 'train')))))
  classes_map = {}
  for idx, cls_train in enumerate(classes_train):
	  classes_map[cls_train] = idx

  with contextlib2.ExitStack() as tf_record_close_stack:
	  train_writer=dataset_utils.open_sharded_output_tfrecords(
			tf_record_close_stack, training_filename, _NUM_TRAIN_FILES)
			
	  _create_tfrecord(dataset_dir, train_writer, classes_map)
	  
  labels_to_class_names = dict(zip(range(len(classes_train)), classes_train))
  dataset_utils.write_label_file(labels_to_class_names, dataset_dir)

if __name__ == '__main__':
	run('./data')