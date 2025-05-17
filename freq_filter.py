import numpy as np
import cv2
import matplotlib.pyplot as plt

def apply_filter(img_path, filter_type, D0, n=2):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    nr, nc = img.shape


    dft = np.fft.fft2(img)
    dft_shift = np.fft.fftshift(dft)

    u = np.arange(nr).reshape(nr, 1)
    v = np.arange(nc).reshape(1, nc)
    dist = np.sqrt((u - nr / 2) ** 2 + (v - nc / 2) ** 2)

    if filter_type == "ideal_lowpass":
        H = np.where(dist <= D0, 1.0, 0.0)
    elif filter_type == "ideal_highpass":
        H = np.where(dist > D0, 1.0, 0.0)
    elif filter_type == "gaussian_lowpass":
        H = np.exp(-(dist**2) / (2 * (D0**2)))
    elif filter_type == "gaussian_highpass":
        H = 1 - np.exp(-(dist**2) / (2 * (D0**2)))
    elif filter_type == "butterworth_lowpass":
        H = 1 / (1 + (dist / D0) ** (2 * n))
    elif filter_type == "butterworth_highpass":
        H = 1 - 1 / (1 + (dist / D0) ** (2 * n))
    else:
        raise ValueError("未知滤波器类型")


    filtered_dft = dft_shift * H

    dft_ishift = np.fft.ifftshift(filtered_dft)
    img_filtered = np.fft.ifft2(dft_ishift)
    img_filtered = np.abs(img_filtered)


    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1), plt.imshow(img, cmap='gray'), plt.title('original')
    plt.subplot(1, 2, 2), plt.imshow(img_filtered, cmap='gray'), plt.title(f'{filter_type} (D0={D0})')
    plt.show()


image_path = r"D:\computer_version\image\lena.jpg"

apply_filter(image_path, "ideal_lowpass", 50)
apply_filter(image_path, "ideal_highpass", 50)
apply_filter(image_path, "gaussian_lowpass", 50)
apply_filter(image_path, "gaussian_highpass", 50)
apply_filter(image_path, "butterworth_lowpass", 50, n=2)
apply_filter(image_path, "butterworth_highpass", 50, n=2)
