import os
import zipfile
import numpy as np
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# # Download url of normal CT scans.
# url = "https://github.com/hasibzunair/3D-image-classification-tutorial/releases/download/v0.2/CT-0.zip"
# filename = os.path.join(os.getcwd(), "CT-0.zip")
# keras.utils.get_file(filename, url)

# # Download url of abnormal CT scans.
# url = "https://github.com/hasibzunair/3D-image-classification-tutorial/releases/download/v0.2/CT-23.zip"
# filename = os.path.join(os.getcwd(), "CT-23.zip")
# keras.utils.get_file(filename, url)

# # Make a directory to store the data.
# # os.makedirs("MosMedData")

# Unzip data in the newly created directory.
with zipfile.ZipFile("CT-0.zip", "r") as z_fp:
    z_fp.extractall("./MosMedData/")

with zipfile.ZipFile("CT-23.zip", "r") as z_fp:
    z_fp.extractall("./MosMedData/")

import nibabel as nib

from scipy import ndimage


def read_nifti_file(filepath):
    """Read and load volume"""
    # Read file
    scan = nib.load(filepath)
    # Get raw data
    scan = scan.get_fdata()
    return scan


def normalize(volume):
    """Normalize the volume"""
    min = -1000
    max = 400
    volume[volume < min] = min
    volume[volume > max] = max
    volume = (volume - min) / (max - min)
    volume = volume.astype("float32")
    return volume


def resize_volume(img):
    """Resize across z-axis"""
    # Set the desired depth
    desired_depth = 64
    desired_width = 256
    desired_height = 256
    # Get current depth
    current_depth = img.shape[-1]
    current_width = img.shape[0]
    current_height = img.shape[1]
    # Compute depth factor
    depth = current_depth / desired_depth
    width = current_width / desired_width
    height = current_height / desired_height
    depth_factor = 1 / depth
    width_factor = 1 / width
    height_factor = 1 / height
    # Rotate
    img = ndimage.rotate(img, 90, reshape=False)
    # Resize across z-axis
    img = ndimage.zoom(img, (width_factor, height_factor, depth_factor), order=1)
    return img


def process_scan(path):
    """Read and resize volume"""
    # Read scan
    volume = read_nifti_file(path)
    # Normalize
    volume = normalize(volume)
    # Resize width, height and depth
    volume = resize_volume(volume)
    return volume

# Folder "CT-0" consist of CT scans having normal lung tissue,
# no CT-signs of viral pneumonia.
normal_scan_paths = [
    os.path.join(os.getcwd(), "MosMedData/CT-0", x)
    for x in os.listdir("MosMedData/CT-0")
]
# Folder "CT-23" consist of CT scans having several ground-glass opacifications,
# involvement of lung parenchyma.
abnormal_scan_paths = [
    os.path.join(os.getcwd(), "MosMedData/CT-23", x)
    for x in os.listdir("MosMedData/CT-23")
]

print("CT scans with normal lung tissue: " + str(len(normal_scan_paths)))
print("CT scans with abnormal lung tissue: " + str(len(abnormal_scan_paths)))

# # Read and process the scans.
# # Each scan is resized across height, width, and depth and rescaled.
# abnormal_scans = np.array([process_scan(path) for path in abnormal_scan_paths])
# normal_scans = np.array([process_scan(path) for path in normal_scan_paths])

# # For the CT scans having presence of viral pneumonia
# # assign 1, for the normal ones assign 0.
# abnormal_labels = np.array([1 for _ in range(len(abnormal_scans))])
# normal_labels = np.array([0 for _ in range(len(normal_scans))])

# # Split data in the ratio 70-30 for training and validation.
# x_train = np.concatenate((abnormal_scans[:70], normal_scans[:70]), axis=0)
# y_train = np.concatenate((abnormal_labels[:70], normal_labels[:70]), axis=0)
# x_val = np.concatenate((abnormal_scans[70:], normal_scans[70:]), axis=0)
# y_val = np.concatenate((abnormal_labels[70:], normal_labels[70:]), axis=0)
# print(
#     "Number of samples in train and validation are %d and %d."
#     % (x_train.shape[0], x_val.shape[0])
# )
path = abnormal_scan_paths[0]
scan_to_visualize = process_scan(path)
# scan_to_visualize = read_nifti_file(path)
def update_slice(num):
    plt.clf()  # Limpiar la figura antes de agregar un nuevo cuadro
    plt.imshow(scan_to_visualize[:, :, num], cmap='gray')  # Mostrar una rebanada en la posición 'num'
    plt.title('CT Scan Slice {}'.format(num))
    plt.axis('off')

# Crear la figura
fig = plt.figure()
# Crear la animación llamando a la función 'update_slice' para cada cuadro
ani = animation.FuncAnimation(fig, update_slice, frames=scan_to_visualize.shape[2], interval=100)

# Mostrar la animación
plt.show()