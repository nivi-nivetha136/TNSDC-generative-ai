# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QmApt3ciNy6JS1QdWaZv3HUa4uN2hGHB
"""

import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

# Define Generator
def build_generator(latent_dim):
    model = models.Sequential()
    model.add(layers.Dense(128, activation='relu', input_dim=latent_dim))
    model.add(layers.Dense(784, activation='sigmoid'))
    model.add(layers.Reshape((28, 28, 1)))
    return model

# Define Discriminator
def build_discriminator():
    model = models.Sequential()
    model.add(layers.Flatten(input_shape=(28, 28, 1)))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model

# Define GAN
def build_gan(generator, discriminator):
    discriminator.trainable = False
    model = models.Sequential()
    model.add(generator)
    model.add(discriminator)
    return model

# Load and preprocess data (MNIST for this example)
(train_images, _), (_, _) = tf.keras.datasets.mnist.load_data()
train_images = train_images.reshape(train_images.shape[0], 28, 28, 1).astype('float32')
train_images = (train_images - 127.5) / 127.5  # Normalize to [-1, 1]

# Define parameters
latent_dim = 100
generator = build_generator(latent_dim)
discriminator = build_discriminator()
gan = build_gan(generator, discriminator)

# Compile models
discriminator.compile(optimizer='adam', loss='binary_crossentropy')
gan.compile(optimizer='adam', loss='binary_crossentropy')

# Training
batch_size = 64
epochs = 10000
for epoch in range(epochs):
    # Train discriminator
    noise = np.random.normal(0, 1, (batch_size, latent_dim))
    fake_images = generator.predict(noise)
    real_images = train_images[np.random.randint(0, train_images.shape[0], batch_size)]
    combined_images = np.concatenate([fake_images, real_images])
    labels = np.concatenate([np.zeros((batch_size, 1)), np.ones((batch_size, 1))])
    labels += 0.05 * np.random.random(labels.shape)  # Add noise to labels
    discriminator_loss = discriminator.train_on_batch(combined_images, labels)

    # Train generator
    noise = np.random.normal(0, 1, (batch_size, latent_dim))
    misleading_labels = np.ones((batch_size, 1))
    generator_loss = gan.train_on_batch(noise, misleading_labels)

    # Print progress
    if epoch % 100 == 0:
        print(f"Epoch: {epoch}, Discriminator Loss: {discriminator_loss}, Generator Loss: {generator_loss}")

# Generate some images
import matplotlib.pyplot as plt
noise = np.random.normal(0, 1, (10, latent_dim))
generated_images = generator.predict(noise)

plt.figure(figsize=(10, 10))
for i in range(generated_images.shape[0]):
    plt.subplot(1, 10, i+1)
    plt.imshow(generated_images[i, :, :, 0], cmap='gray')
    plt.axis('off')
plt.show()