

# Use numpy array as std return type 

import matplotlib.pyplot as plt
import numpy as np
import os, os.path
import PIL
import PIL.Image as img
import colorsys # Saturation operation 
import cv2

baselinePath = ".//Images//gradient.jpg"

def ReadBaseImage():
    
    print(os.getcwd())
    image = img.open(os.getcwd()+baselinePath).convert("RGB")
    image = np.array(image)
    return image 


def ReadBaseImageRGB():
    image = cv2.imread(baselinePath)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return rgb_image

def ConvertToHSV(CV2Img):
    return cv2.cvtColor(CV2Img, cv2.COLOR_RGB2HSV)


def Display(npImageArray):
    image = img.fromarray(npImageArray)
    plt.imshow(image)
    plt.axis('off')  # Turn off axis labels
    plt.show()



def ConvertSaturation(npImageArray):
    image = img.fromarray(npImageArray)
    saturation_matrix = np.zeros((image.shape[0], image.shape[1]))
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            r, g, b = pixels[i, j] / 255.0  # Normalize RGB to [0, 1]
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            saturation_matrix[i, j] = s  # Store saturation value

def create_lookup_table(gamma):
    #inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** gamma 
                      * 255 for i in np.arange(0, 256)]).astype("uint8")
    return table



def DisplaySaturation(hsvImg, surpressDisplay = False ):
    saturation_channel = hsvImg[:, :, 1]

    # Normalize the saturation values to range [0, 255] (as they are originally in [0, 255])
    saturation_normalized = saturation_channel.astype(np.uint8)

    bw_image = cv2.merge([saturation_normalized, saturation_normalized, saturation_normalized])

    npArrayForm = np.array(bw_image)

    if (surpressDisplay):
        Display(npArrayForm)

    return npArrayForm

def img_is_color(img):

    if len(img.shape) == 3:
        # Check the color channels to see if they're all the same.
        c1, c2, c3 = img[:, : , 0], img[:, :, 1], img[:, :, 2]
        if (c1 == c2).all() and (c2 == c3).all():
            return True

    return False

def show_image_list(list_images, list_titles=None, 
                    list_cmaps=None, grid=True, 
                    num_cols=2, figsize=(20, 10), title_fontsize=30):
    '''
    Shows a grid of images, where each image is a Numpy array. The images can be either
    RGB or grayscale.

    Parameters:
    ----------
    images: list
        List of the images to be displayed.
    list_titles: list or None
        Optional list of titles to be shown for each image.
    list_cmaps: list or None
        Optional list of cmap values for each image. If None, then cmap will be
        automatically inferred.
    grid: boolean
        If True, show a grid over each image
    num_cols: int
        Number of columns to show.
    figsize: tuple of width, height
        Value to be passed to pyplot.figure()
    title_fontsize: int
        Value to be passed to set_title().
    '''

    assert isinstance(list_images, list)
    assert len(list_images) > 0
    assert isinstance(list_images[0], np.ndarray)

    if list_titles is not None:
        assert isinstance(list_titles, list)
        assert len(list_images) == len(list_titles), '%d imgs != %d titles' % (len(list_images), len(list_titles))

    if list_cmaps is not None:
        assert isinstance(list_cmaps, list)
        assert len(list_images) == len(list_cmaps), '%d imgs != %d cmaps' % (len(list_images), len(list_cmaps))

    num_images  = len(list_images)
    num_cols    = min(num_images, num_cols)
    num_rows    = int(num_images / num_cols) + (1 if num_images % num_cols != 0 else 0)

    # Create a grid of subplots.
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    
    # Create list of axes for easy iteration.
    if isinstance(axes, np.ndarray):
        list_axes = list(axes.flat)
    else:
        list_axes = [axes]

    for i in range(num_images):

        img    = list_images[i]
        title  = list_titles[i] if list_titles is not None else 'Image %d' % (i)
        cmap   = list_cmaps[i] if list_cmaps is not None else (None if img_is_color(img) else 'gray')
        
        list_axes[i].imshow(img, cmap=cmap)
        list_axes[i].set_title(title, fontsize=title_fontsize) 
        list_axes[i].grid(grid)

    for i in range(num_images, len(list_axes)):
        list_axes[i].set_visible(False)

    fig.tight_layout()
    _ = plt.show()


def main():
    base = ReadBaseImageRGB()
    hsvImg = ConvertToHSV(base)

    gamma = 2.2  # Example gamma value for the curve
    lookup_table = create_lookup_table(gamma)
    bgrAdjImg = cv2.LUT(base, lookup_table)

    rgbAdjImg = cv2.cvtColor(bgrAdjImg, cv2.COLOR_BGR2RGB)
    curvedHsvImg = ConvertToHSV(rgbAdjImg)

    original = DisplaySaturation(hsvImg)
    curved = DisplaySaturation(curvedHsvImg)

    show_image_list([base, bgrAdjImg, original, curved], 
                    ["Original", "Curved", "Original S", "Curved S"],
                    grid = False, 
                    figsize=(10, 10), 
                    title_fontsize = 20)

main()