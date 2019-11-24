#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import glob
import logging.handlers
import os

import tensorflow as tf
from tqdm import trange

from .const import TRAIN_PATH, LOGS_Path, CHECKPOINTS_PATH
from .model_utils import get_img_batch, denormalize_batch

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/model.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


class DeepStegano:
    def __init__(self, epochs=100, batch_size=8, learning_rate=0.0001, beta=0.75):
        self.epochs = epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.beta = beta
        self.sess = None
        self.deploy_hide_image_op = None
        self.deploy_reveal_image_op = None
        self.train_op = None
        self.summary_op = None
        self.test_op = None
        self.global_step_tensor = None

    @staticmethod
    def get_prep_network_op(secret_tensor):
        with tf.variable_scope('prep_net'):
            with tf.variable_scope("3x3_conv_branch"):
                conv_3x3 = tf.layers.conv2d(inputs=secret_tensor, filters=50, kernel_size=3, padding='same', name="1",
                                            activation=tf.nn.relu)
                conv_3x3 = tf.layers.conv2d(inputs=conv_3x3, filters=50, kernel_size=3, padding='same', name="2",
                                            activation=tf.nn.relu)
                conv_3x3 = tf.layers.conv2d(inputs=conv_3x3, filters=50, kernel_size=3, padding='same', name="3",
                                            activation=tf.nn.relu)
                conv_3x3 = tf.layers.conv2d(inputs=conv_3x3, filters=50, kernel_size=3, padding='same', name="4",
                                            activation=tf.nn.relu)

            with tf.variable_scope("4x4_conv_branch"):
                conv_4x4 = tf.layers.conv2d(inputs=secret_tensor, filters=50, kernel_size=4, padding='same', name="1",
                                            activation=tf.nn.relu)
                conv_4x4 = tf.layers.conv2d(inputs=conv_4x4, filters=50, kernel_size=4, padding='same', name="2",
                                            activation=tf.nn.relu)
                conv_4x4 = tf.layers.conv2d(inputs=conv_4x4, filters=50, kernel_size=4, padding='same', name="3",
                                            activation=tf.nn.relu)
                conv_4x4 = tf.layers.conv2d(inputs=conv_4x4, filters=50, kernel_size=4, padding='same', name="4",
                                            activation=tf.nn.relu)

            with tf.variable_scope("5x5_conv_branch"):
                conv_5x5 = tf.layers.conv2d(inputs=secret_tensor, filters=50, kernel_size=5, padding='same', name="1",
                                            activation=tf.nn.relu)
                conv_5x5 = tf.layers.conv2d(inputs=conv_5x5, filters=50, kernel_size=5, padding='same', name="2",
                                            activation=tf.nn.relu)
                conv_5x5 = tf.layers.conv2d(inputs=conv_5x5, filters=50, kernel_size=5, padding='same', name="3",
                                            activation=tf.nn.relu)
                conv_5x5 = tf.layers.conv2d(inputs=conv_5x5, filters=50, kernel_size=5, padding='same', name="4",
                                            activation=tf.nn.relu)

            concat_1 = tf.concat([conv_3x3, conv_4x4, conv_5x5], axis=3, name='concat_1')

            conv_5x5 = tf.layers.conv2d(inputs=concat_1, filters=50, kernel_size=5, padding='same', name="final_5x5",
                                        activation=tf.nn.relu)
            conv_4x4 = tf.layers.conv2d(inputs=concat_1, filters=50, kernel_size=4, padding='same', name="final_4x4",
                                        activation=tf.nn.relu)
            conv_3x3 = tf.layers.conv2d(inputs=concat_1, filters=50, kernel_size=3, padding='same', name="final_3x3",
                                        activation=tf.nn.relu)

            concat_final = tf.concat([conv_5x5, conv_4x4, conv_3x3], axis=3, name='concat_final')

            return concat_final

    @staticmethod
    def get_hiding_network_op(cover_tensor, prep_output):
        with tf.variable_scope('hide_net'):
            concat_input = tf.concat([cover_tensor, prep_output], axis=3, name='images_features_concat')

            with tf.variable_scope("3x3_conv_branch"):
                conv_3x3 = tf.layers.conv2d(inputs=concat_input, filters=50, kernel_size=3, padding='same', name="1",
                                            activation=tf.nn.relu)
                conv_3x3 = tf.layers.conv2d(inputs=conv_3x3, filters=50, kernel_size=3, padding='same', name="2",
                                            activation=tf.nn.relu)
                conv_3x3 = tf.layers.conv2d(inputs=conv_3x3, filters=50, kernel_size=3, padding='same', name="3",
                                            activation=tf.nn.relu)
                conv_3x3 = tf.layers.conv2d(inputs=conv_3x3, filters=50, kernel_size=3, padding='same', name="4",
                                            activation=tf.nn.relu)

            with tf.variable_scope("4x4_conv_branch"):
                conv_4x4 = tf.layers.conv2d(inputs=concat_input, filters=50, kernel_size=4, padding='same', name="1",
                                            activation=tf.nn.relu)
                conv_4x4 = tf.layers.conv2d(inputs=conv_4x4, filters=50, kernel_size=4, padding='same', name="2",
                                            activation=tf.nn.relu)
                conv_4x4 = tf.layers.conv2d(inputs=conv_4x4, filters=50, kernel_size=4, padding='same', name="3",
                                            activation=tf.nn.relu)
                conv_4x4 = tf.layers.conv2d(inputs=conv_4x4, filters=50, kernel_size=4, padding='same', name="4",
                                            activation=tf.nn.relu)

            with tf.variable_scope("5x5_conv_branch"):
                conv_5x5 = tf.layers.conv2d(inputs=concat_input, filters=50, kernel_size=5, padding='same', name="1",
                                            activation=tf.nn.relu)
                conv_5x5 = tf.layers.conv2d(inputs=conv_5x5, filters=50, kernel_size=5, padding='same', name="2",
                                            activation=tf.nn.relu)
                conv_5x5 = tf.layers.conv2d(inputs=conv_5x5, filters=50, kernel_size=5, padding='same', name="3",
                                            activation=tf.nn.relu)
                conv_5x5 = tf.layers.conv2d(inputs=conv_5x5, filters=50, kernel_size=5, padding='same', name="4",
                                            activation=tf.nn.relu)

            concat_1 = tf.concat([conv_3x3, conv_4x4, conv_5x5], axis=3, name='concat_1')

            conv_5x5 = tf.layers.conv2d(inputs=concat_1, filters=50, kernel_size=5, padding='same', name="final_5x5",
                                        activation=tf.nn.relu)
            conv_4x4 = tf.layers.conv2d(inputs=concat_1, filters=50, kernel_size=4, padding='same', name="final_4x4",
                                        activation=tf.nn.relu)
            conv_3x3 = tf.layers.conv2d(inputs=concat_1, filters=50, kernel_size=3, padding='same', name="final_3x3",
                                        activation=tf.nn.relu)

            concat_final = tf.concat([conv_5x5, conv_4x4, conv_3x3], axis=3, name='concat_final')
            output = tf.layers.conv2d(inputs=concat_final, filters=3, kernel_size=1, padding='same', name='output')

            return output

    @staticmethod
    def get_reveal_network_op(container_tensor):
        with tf.variable_scope('reveal_net'):
            with tf.variable_scope("3x3_conv_branch"):
                conv_3x3 = tf.layers.conv2d(inputs=container_tensor, filters=50, kernel_size=3, padding='same',
                                            name="1",
                                            activation=tf.nn.relu)
                conv_3x3 = tf.layers.conv2d(inputs=conv_3x3, filters=50, kernel_size=3, padding='same', name="2",
                                            activation=tf.nn.relu)
                conv_3x3 = tf.layers.conv2d(inputs=conv_3x3, filters=50, kernel_size=3, padding='same', name="3",
                                            activation=tf.nn.relu)
                conv_3x3 = tf.layers.conv2d(inputs=conv_3x3, filters=50, kernel_size=3, padding='same', name="4",
                                            activation=tf.nn.relu)

            with tf.variable_scope("4x4_conv_branch"):
                conv_4x4 = tf.layers.conv2d(inputs=container_tensor, filters=50, kernel_size=4, padding='same',
                                            name="1",
                                            activation=tf.nn.relu)
                conv_4x4 = tf.layers.conv2d(inputs=conv_4x4, filters=50, kernel_size=4, padding='same', name="2",
                                            activation=tf.nn.relu)
                conv_4x4 = tf.layers.conv2d(inputs=conv_4x4, filters=50, kernel_size=4, padding='same', name="3",
                                            activation=tf.nn.relu)
                conv_4x4 = tf.layers.conv2d(inputs=conv_4x4, filters=50, kernel_size=4, padding='same', name="4",
                                            activation=tf.nn.relu)

            with tf.variable_scope("5x5_conv_branch"):
                conv_5x5 = tf.layers.conv2d(inputs=container_tensor, filters=50, kernel_size=5, padding='same',
                                            name="1",
                                            activation=tf.nn.relu)
                conv_5x5 = tf.layers.conv2d(inputs=conv_5x5, filters=50, kernel_size=5, padding='same', name="2",
                                            activation=tf.nn.relu)
                conv_5x5 = tf.layers.conv2d(inputs=conv_5x5, filters=50, kernel_size=5, padding='same', name="3",
                                            activation=tf.nn.relu)
                conv_5x5 = tf.layers.conv2d(inputs=conv_5x5, filters=50, kernel_size=5, padding='same', name="4",
                                            activation=tf.nn.relu)

            concat_1 = tf.concat([conv_3x3, conv_4x4, conv_5x5], axis=3, name='concat_1')

            conv_5x5 = tf.layers.conv2d(inputs=concat_1, filters=50, kernel_size=5, padding='same', name="final_5x5",
                                        activation=tf.nn.relu)
            conv_4x4 = tf.layers.conv2d(inputs=concat_1, filters=50, kernel_size=4, padding='same', name="final_4x4",
                                        activation=tf.nn.relu)
            conv_3x3 = tf.layers.conv2d(inputs=concat_1, filters=50, kernel_size=3, padding='same', name="final_3x3",
                                        activation=tf.nn.relu)

            concat_final = tf.concat([conv_5x5, conv_4x4, conv_3x3], axis=3, name='concat_final')

        output = tf.layers.conv2d(inputs=concat_final, filters=3, kernel_size=1, padding='same', name='output')

        return output

    @staticmethod
    def get_noise_layer_op(tensor, std=.1):
        with tf.variable_scope("noise_layer"):
            return tensor + tf.random_normal(shape=tf.shape(tensor), mean=0.0, stddev=std, dtype=tf.float32)

    @staticmethod
    def get_loss_op(secret_true, secret_pred, cover_true, cover_pred, beta=.5):
        with tf.variable_scope("losses"):
            beta = tf.constant(beta, name="beta")
            secret_mse = tf.losses.mean_squared_error(secret_true, secret_pred)
            cover_mse = tf.losses.mean_squared_error(cover_true, cover_pred)
            final_loss = cover_mse + beta * secret_mse
            return final_loss, secret_mse, cover_mse

    @staticmethod
    def get_tensor_to_img_op(tensor):
        with tf.variable_scope("", reuse=True):
            t = tensor * tf.convert_to_tensor([0.229, 0.224, 0.225]) + tf.convert_to_tensor([0.485, 0.456, 0.406])
            return tf.clip_by_value(t, 0, 1)

    def prepare_training_graph(self, secret_tensor, cover_tensor, global_step_tensor):
        prep_output_op = self.get_prep_network_op(secret_tensor)
        hiding_output_op = self.get_hiding_network_op(cover_tensor=cover_tensor, prep_output=prep_output_op)
        noise_add_op = self.get_noise_layer_op(hiding_output_op)
        reveal_output_op = self.get_reveal_network_op(noise_add_op)

        loss_op, secret_loss_op, cover_loss_op = self.get_loss_op(secret_tensor, reveal_output_op, cover_tensor,
                                                                  hiding_output_op, beta=self.beta)

        minimize_op = tf.train.AdamOptimizer(self.learning_rate).minimize(loss_op, global_step=global_step_tensor)

        tf.summary.scalar('loss', loss_op, family='train')
        tf.summary.scalar('reveal_net_loss', secret_loss_op, family='train')
        tf.summary.scalar('cover_net_loss', cover_loss_op, family='train')

        tf.summary.image('secret', self.get_tensor_to_img_op(secret_tensor), max_outputs=1, family='train')
        tf.summary.image('cover', self.get_tensor_to_img_op(cover_tensor), max_outputs=1, family='train')
        tf.summary.image('hidden', self.get_tensor_to_img_op(hiding_output_op), max_outputs=1, family='train')
        tf.summary.image('hidden_noisy', self.get_tensor_to_img_op(noise_add_op), max_outputs=1, family='train')
        tf.summary.image('revealed', self.get_tensor_to_img_op(reveal_output_op), max_outputs=1, family='train')

        merged_summary_op = tf.summary.merge_all()

        return minimize_op, merged_summary_op

    def prepare_test_graph(self, secret_tensor, cover_tensor):
        with tf.variable_scope("", reuse=True):
            prep_output_op = self.get_prep_network_op(secret_tensor)
            hiding_output_op = self.get_hiding_network_op(cover_tensor=cover_tensor, prep_output=prep_output_op)
            reveal_output_op = self.get_reveal_network_op(hiding_output_op)

            loss_op, secret_loss_op, cover_loss_op = self.get_loss_op(secret_tensor, reveal_output_op, cover_tensor,
                                                                      hiding_output_op)

            tf.summary.scalar('loss', loss_op, family='test')
            tf.summary.scalar('reveal_net_loss', secret_loss_op, family='test')
            tf.summary.scalar('cover_net_loss', cover_loss_op, family='test')

            tf.summary.image('secret', self.get_tensor_to_img_op(secret_tensor), max_outputs=1, family='test')
            tf.summary.image('cover', self.get_tensor_to_img_op(cover_tensor), max_outputs=1, family='test')
            tf.summary.image('hidden', self.get_tensor_to_img_op(hiding_output_op), max_outputs=1, family='test')
            tf.summary.image('revealed', self.get_tensor_to_img_op(reveal_output_op), max_outputs=1, family='test')

            merged_summary_op = tf.summary.merge_all()

            return merged_summary_op

    def prepare_deployment_graph(self, secret_tensor, cover_tensor, covered_tensor):
        with tf.variable_scope("", reuse=True):
            prep_output_op = self.get_prep_network_op(secret_tensor)
            self.deploy_hide_image_op = self.get_hiding_network_op(cover_tensor=cover_tensor,
                                                                   prep_output=prep_output_op)
            self.deploy_reveal_image_op = self.get_reveal_network_op(covered_tensor)

    def init_model(self):
        self.sess = tf.InteractiveSession(graph=tf.Graph())

        secret_tensor = tf.placeholder(shape=[None, 224, 224, 3], dtype=tf.float32, name="input_prep")
        cover_tensor = tf.placeholder(shape=[None, 224, 224, 3], dtype=tf.float32, name="input_hide")
        self.global_step_tensor = tf.Variable(0, trainable=False, name='global_step')

        self.train_op, self.summary_op = self.prepare_training_graph(secret_tensor, cover_tensor,
                                                                     self.global_step_tensor)

        self.test_op = self.prepare_test_graph(secret_tensor, cover_tensor)

        covered_tensor = tf.placeholder(shape=[None, 224, 224, 3], dtype=tf.float32, name="deploy_covered")
        self.prepare_deployment_graph(secret_tensor, cover_tensor, covered_tensor)

        self.sess.run(tf.global_variables_initializer())

    def train(self):
        """

        :param epochs:
        :param batch_size:
        :param learning_rate:
        :param beta:
        :return:
        """
        experience_name = "beta_{}".format(self.beta)
        self.init_model()
        saver = tf.train.Saver()
        writer = tf.summary.FileWriter(os.path.join(LOGS_Path, experience_name), self.sess.graph)
        files_list = glob.glob(os.path.join(TRAIN_PATH, "*.jpg"))
        total_steps = len(files_list) // self.batch_size + 1

        # Train
        for _ in trange(self.epochs, desc='Epochs'):
            for step in trange(total_steps, desc='steps'):
                covers, secrets = get_img_batch(files_list=files_list, batch_size=self.batch_size)
                self.sess.run([self.train_op], feed_dict={"input_prep:0": secrets, "input_hide:0": covers})

                if step % 10 == 0:
                    summary, global_step = self.sess.run([self.summary_op, self.global_step_tensor],
                                                         feed_dict={"input_prep:0": secrets, "input_hide:0": covers})
                    writer.add_summary(summary, global_step)

                if step % 100 == 0:
                    covers, secrets = \
                        get_img_batch(files_list=files_list, batch_size=1)
                    summary, global_step = self.sess.run([self.test_op, self.global_step_tensor],
                                                         feed_dict={"input_prep:0": secrets, "input_hide:0": covers})
                    writer.add_summary(summary, global_step)

            saver.save(self.sess, os.path.join(CHECKPOINTS_PATH, experience_name), global_step=global_step)

        writer.close()

    def load_model(self, checkpoint_path):

        self.init_model()
        saver = tf.train.Saver()
        saver.restore(self.sess, tf.train.latest_checkpoint(checkpoint_path))

    def run_model(self, cover, secret):

        if self.sess is None or self.deploy_reveal_image_op is None:
            raise ValueError("Nee to init the model by running load_model")
        hidden = self.sess.run(self.deploy_hide_image_op, feed_dict={'input_prep:0': secret, 'input_hide:0': cover})
        revealed = self.sess.run(self.deploy_reveal_image_op, feed_dict={'deploy_covered:0': hidden})
        return denormalize_batch(hidden.squeeze()) * 255, denormalize_batch(revealed.squeeze()) * 255

    def revealed_image(self, image):
        if self.sess is None or self.deploy_reveal_image_op is None:
            raise ValueError("Nee to init the model by running load_model")
        revealed = self.sess.run(self.deploy_reveal_image_op, feed_dict={'deploy_covered:0': image})
        return denormalize_batch(revealed.squeeze()) * 255
