from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from os.path import join
import glob
import sys
import contextlib2
from random import shuffle

import numpy as np
import cv2
from six.moves import cPickle
from six.moves import urllib
import tensorflow as tf

import dataset_utils


_NUM_TRAIN_FILES = 1


def _create_tfrecord_train(dataset_dir, tfrecord_writer, classes_train):
	count = 0
	all_image_paths, class_labels = [], []
	for cls_train in classes_train:
		images_dir = glob.glob(join(dataset_dir, 'train', cls_train, '*.JPG'))
		all_image_paths.extend(images_dir)
		class_labels.extend([classes_train[cls_train] for _ in range(len(images_dir))])

	combined = list(zip(all_image_paths, class_labels))
	shuffle(combined)
	all_image_paths, class_labels = zip(*combined)

	for i, im_path in enumerate(all_image_paths):
		with tf.gfile.Open(im_path, 'rb') as f:
			img = cv2.imread(im_path)
			img_shape = img.shape
			if img_shape != (256, 256, 3):
				img = cv2.resize(img, (256, 256))
			_, encoded_image = cv2.imencode('.jpg', img)
			label = class_labels[i]
			encoded_image = encoded_image.tobytes()
			example = dataset_utils.image_to_tfexample(
        		encoded_image, b'jpg', 256, 256, label)

			output_shard_index = count % _NUM_TRAIN_FILES
			tfrecord_writer[output_shard_index].write(example.SerializeToString())
			count += 1
			print('Processed {} images'.format(count))


def _create_tfrecord_test(dataset_dir, tfrecord_writer, classes_train):
	count = 0
	image_paths = sorted(glob.glob(join(dataset_dir, 'test_imgs', '*.JPG')))
	num_images =  len(image_paths)
	for i, im_path in enumerate(image_paths):
		with tf.gfile.Open(im_path, 'rb') as f:
			img = cv2.imread(im_path)
			img_shape = img.shape
			if img_shape != (256, 256, 3):
				img = cv2.resize(img, (256, 256))
			_, encoded_image = cv2.imencode('.jpg', img)
			encoded_image = encoded_image.tobytes()
			example = dataset_utils.image_to_tfexample(
        		encoded_image, b'jpg', 256, 256, 0)

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
  return '%s/pc_%s' % (dataset_dir, split_name)


def run(dataset_dir):
  """Runs the download and conversion operation.
  Args:
	dataset_dir: The dataset directory where the dataset is stored.
  """
  if not tf.gfile.Exists(dataset_dir):
	  tf.gfile.MakeDirs(dataset_dir)

  training_filename = _get_output_filename(dataset_dir, 'train')
  testing_filename = _get_output_filename(dataset_dir, 'val')
  
  classes_train = sorted(list(filter(lambda x: os.path.isdir(join(dataset_dir, 'train', x)), os.listdir(join(dataset_dir, 'train')))))
  classes_map = {}
  for idx, cls_train in enumerate(classes_train):
	  classes_map[cls_train] = idx

  with contextlib2.ExitStack() as tf_record_close_stack:
 	  train_writer=dataset_utils.open_sharded_output_tfrecords(
    		tf_record_close_stack, training_filename, _NUM_TRAIN_FILES)
 	  _create_tfrecord_train(dataset_dir, train_writer, classes_map)

  with contextlib2.ExitStack() as tf_record_close_stack:
	  test_writer=dataset_utils.open_sharded_output_tfrecords(
			tf_record_close_stack, testing_filename, _NUM_TRAIN_FILES)
	  _create_tfrecord_test(dataset_dir, test_writer, classes_map)

  labels_to_class_names = dict(zip(range(len(classes_train)), classes_train))
  dataset_utils.write_label_file(labels_to_class_names, dataset_dir)

if __name__ == '__main__':
	run('./data')
