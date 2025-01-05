import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
import os


def shuffle_pic(image_path, block_size=16):
    # 将转换后的图片存储在图片所在目录下的random_shuffle目录下
    save_path = os.path.join(os.path.dirname(image_path), 'random_shuffle')
    # make sure dir exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    new_image_path = os.path.join(save_path, os.path.basename(image_path))
    
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)
    height, width = image_array.shape
    assert height % block_size == 0 and width % block_size == 0, "图片尺寸必须是8的倍数"
    blocks = []
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = image_array[i:i+block_size, j:j+block_size]
            blocks.append(block)
    random.shuffle(blocks)
    new_image_array = np.zeros_like(image_array)
    index = 0
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            new_image_array[i:i+block_size, j:j+block_size] = blocks[index]
            index += 1
    new_image = Image.fromarray(new_image_array)
    plt.axis('off')  # 关闭坐标轴
    plt.imsave(new_image_path, new_image,cmap='gray')

base_path = "/mnt/d/CodeHome/tiny-codec/tinyimgcodec/data"
for file in os.listdir(base_path):
    if file.endswith(".gif"):
        shuffle_pic(os.path.join(base_path, file))