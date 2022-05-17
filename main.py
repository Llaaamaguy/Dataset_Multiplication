from PIL import Image, ImageEnhance
import cv2 as cv
import numpy as np
import random
from alive_progress import alive_bar
import os


def add_noise(image):
    row, col, ch = image.shape
    number_of_pixels = random.randint(300, 10000)

    for i in range(number_of_pixels):
        y_coord = random.randint(0, row - 1)
        x_coord = random.randint(0, col - 1)
        image[y_coord][x_coord] = 255

    number_of_pixels = random.randint(300, 10000)
    for i in range(number_of_pixels):
        y_coord = random.randint(0, row - 1)
        x_coord = random.randint(0, col - 1)
        image[y_coord][x_coord] = 0

    return image


def multiply_image(fname, dir):
    kernel_sharpening = np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ])

    pimg = Image.open(f"{dir}{fname}")
    enhanced = ImageEnhance.Contrast(pimg)
    enhanced.enhance(1.8).save(f"{dir}enhanced{fname}")
    pimg = cv.imread(f"{dir}enhanced{fname}")

    cimg = cv.imread(f"{dir}{fname}")
    flipped = cv.flip(cimg, 1)
    cv.imwrite(f"{dir}flipped{fname}", flipped)

    toManip = {"img": cimg, "flip": flipped, "psharp": pimg}

    for mode, img in toManip.items():
        blurred = cv.GaussianBlur(img, (9, 9), 0)
        cv.imwrite(f"{dir}blurred{mode+fname}", blurred)

        sharpened = cv.filter2D(img, -1, kernel_sharpening)
        cv.imwrite(f"{dir}sharp{mode+fname}", sharpened)

        noised = add_noise(img)
        cv.imwrite(f"{dir}noise{mode+fname}", noised)

        blurSharp = cv.filter2D(blurred, -1, kernel_sharpening)
        cv.imwrite(f"{dir}blursharp{mode+fname}", blurSharp)

        sharpNoise = add_noise(sharpened)
        cv.imwrite(f"{dir}sharpnoise{mode+fname}", sharpNoise)

        blurNoise = add_noise(blurred)
        cv.imwrite(f"{dir}blurnoise{mode+fname}", blurNoise)

        all = add_noise(blurSharp)
        cv.imwrite(f"{dir}all{mode+fname}", all)


def main():
    dir = "FormData1/"
    with alive_bar(len(os.listdir(dir)[0])*len(os.listdir(dir)), title="Analyzing...") as bar:
        for subdir in os.listdir(dir):
            if subdir != ".DS_Store":
                for image in os.listdir(dir+subdir):
                    if image != ".DS_Store":
                        if image.split(".")[1] != "HEIC":
                            multiply_image(image, (dir+subdir+"/"))
                            bar()


if __name__ == "__main__":
    main()
