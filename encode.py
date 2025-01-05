#!/usr/bin/env python3

import sys
import numpy as np
from PIL import Image
from tinyimgcodec import compress
import os

""" 
# 原始代码
im = Image.open(sys.argv[1]).convert("L")
print(im.size)

out = compress(np.asarray(im), auto_generate_huffman_table=False)

byte_size = len(out)
print(f"{byte_size} bytes")
print(f"Compression Ratio: {im.width * im.height / byte_size}:1")
with open(sys.argv[2], "wb") as f:
    f.write(out) """

def compress_folder(img_folder):
    files = [file for file in os.listdir(img_folder) if file.endswith(".gif")]
    # print(files)
    compression_ratio = []
    for file in files:
        file = os.path.join(img_folder,file)
        file_name = os.path.basename(file)
        
        im = Image.open(file).convert("L")
        
        out = compress(np.asarray(im), auto_generate_huffman_table=False)

        byte_size = len(out)
        
        # print(f"{byte_size} bytes")
        # print(f"Compression Ratio: {im.width * im.height / byte_size}:1")
        compression_ratio.append([file_name,byte_size,im.width * im.height / byte_size])
    return compression_ratio


# 改写，测试shuffle后的图片压缩比的变化，一次性处理一个文件夹中所有gif文件
img_folder = sys.argv[1]
img_folder2 = "/mnt/d/CodeHome/tiny-codec/tinyimgcodec/data/random_shuffle"
compress_ratio1 = compress_folder(img_folder)
compress_ratio2 = compress_folder(img_folder2)

# Save comparison data to a CSV file
import csv
def save_comparison_data_csv(compression_ratio1, compression_ratio2, save_path):
    # Prepare data for CSV
    header = ['File Name', 'Compression Ratio 1', 'Compression Ratio 2']
    rows = []
    
    # Ensure the file names match across both lists (important for comparison)
    sum = 0
    for item1, item2 in zip(compression_ratio1, compression_ratio2):
        if item1[0] == item2[0]:
            rows.append([item1[0], item1[1], item2[1],(item2[1]-item1[1])/item1[1]])
            sum+=(item2[1]-item1[1])/item1[1]
        else:
            print(f"Warning: File name mismatch between the two folders: {item1[0]} != {item2[0]}")
    
    print(sum/len(compression_ratio1))
    # Write data to CSV
    with open(save_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"Data saved to {save_path}")
    
save_comparison_data_csv(compress_ratio1, compress_ratio2, 'compression_ratio_comparison.csv')
# 将两列compression_ratio进行对比
for i in range(len(compress_ratio1)):
    print(f"{compress_ratio1[i][0]} {compress_ratio1[i][1]} {compress_ratio2[i][1]}")
    # 将对比数据通过numpy使用文件的形式保存下来,需要易于读取
