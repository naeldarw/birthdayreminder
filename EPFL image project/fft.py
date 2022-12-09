import time

import numpy
import os
# import tifffile
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import matplotlib.image as image

# directory = 'C:\\Code\\github.com\\naeldarw\\birthdayreminder\\EPFL image project\\21'

focal_size = int  # focus of the microscope when taking the pictures, which depends of the height we take the
# picture at
mm_to_pixel = 3.7795275591  # 1mm in number of pixels
square_real_size = int  # Real size in mm of a side of the square we want to take a picture of


def right_extremum(current_pos: int, fftsum_dic: dict) -> int:  # current_pos is the pos. in list_img
    current_pos += 50
    while not (fftsum_dic[current_pos - 50] > fftsum_dic[current_pos] and fftsum_dic[current_pos + 50] > fftsum_dic[
        current_pos]) and not (
            fftsum_dic[current_pos - 50] < fftsum_dic[current_pos] and fftsum_dic[current_pos + 50] < fftsum_dic[
        current_pos]):
        current_pos += 1
    return current_pos


def left_extremum(current_pos: int, fftsum_dic: dict) -> int:
    current_pos -= 50
    while not (fftsum_dic[current_pos - 50] > fftsum_dic[current_pos] and fftsum_dic[current_pos + 50] > fftsum_dic[
        current_pos]) and not (
            fftsum_dic[current_pos - 50] < fftsum_dic[current_pos] and fftsum_dic[current_pos + 50] < fftsum_dic[
        current_pos]):
        current_pos -= 1
    return current_pos


def find_max_from_3_points(x_1, y_1, x_2, y_2, x_3, y_3):  # return maximum's position
    quadratic = numpy.polyfit((x_1, x_2, x_3), (y_1, y_2, y_3), deg=2)
    a = quadratic[0]
    b = quadratic[1]
    c = quadratic[2]

    x = -b / (2 * a)
    # print(a, b, c)
    print(x, 'x axis position of the maximum sharpness image')

    return x, (a, b, c)


def find_band(rmax: int, rmin: int, x: int, y: int):
    # max_num = ((x / 2) ** 2 + (y / 2) ** 2) ** (1 / 2)
    # min_num = 0
    coords = numpy.mgrid[0:x, 0:y]
    coords = coords.astype(float)
    coords[0] -= x / 2
    coords[1] -= y / 2
    r = numpy.sqrt(coords[0] ** 2 + coords[1] ** 2)
    band = numpy.logical_and(r > rmin, r < rmax)
    return band


def return_height_for_sharpest_square(pic1: str, h1: int, pic2: str, h2: int, pic3: str, h3: int) -> int:
    pic1 = image.imread(pic1)
    pic1_array = numpy.array(pic1).astype(float)
    pic2 = image.imread(pic2)
    pic2_array = numpy.array(pic2).astype(float)
    pic3 = image.imread(pic3)
    pic3_array = numpy.array(pic2).astype(float)
    pic3_array = returns_blured_mask(pic3_array, 0, 160)  # 160 pixels is the average radius of a "tiny" square.
    pic2_array = returns_blured_mask(pic2_array, 0, 160)
    pic1_array = returns_blured_mask(pic1_array, 0, 160)
    x_1, y_1 = h1, take_fft(pic1_array)
    x_2, y_2 = h2, take_fft(pic2_array)
    x_3, y_3 = h3, take_fft(pic3_array)

    sharpest_height, quadratic = find_max_from_3_points(x_1, y_1, x_2, y_2, x_3, y_3)
    return sharpest_height


def move_epsilon(current_height: int, epsilon: int) -> (str, str):
    pass
    # TODO take pictures at current_height +- epsilon and return them as two files


def fft_plot(list_im: list) -> dict:
    height_energy = {}
    for i, img in enumerate(list_im):
        # print(i)
        img = image.imread(img)
        im = numpy.array(img).astype(float)
        # im -= numpy.median(im, axis=(0))
        # height_energy[i] = numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(im)))[band].sum()
        height_energy[i] = numpy.max(im) - numpy.min(im)  # Method that isn't correct but plots a graph similar to the
        # fft graph
    return height_energy


def take_fft(img) -> int:
    img = numpy.fft.fftshift(numpy.fft.fft2(img))
    return sum_fourier_abs(img, 10, 300)


def initialize_list_img(directory: str):
    list_of_imgs = []  # paths of the images

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        list_of_imgs.append(f)
    list_of_imgs = list_of_imgs[::10]
    return list_of_imgs


def get_maximum_sharpness_intervall(fft_height_energy: dict):  # the images are in "directory"

    # band = find_band()  # We assume that all of the images have the same sizes

    height, energy = max([(height, energy) for height, energy in fft_height_energy.items()], key=lambda a: a[1])
    # print(height, energy, 'height-energy')

    nearest_right_side_local_extremum = right_extremum(height, fft_height_energy)
    nearest_left_side_local_extremum = left_extremum(height, fft_height_energy)

    maximum_sharpness_intervall = (nearest_left_side_local_extremum, nearest_right_side_local_extremum)
    distance = nearest_right_side_local_extremum - nearest_left_side_local_extremum

    return maximum_sharpness_intervall, distance


def get_max_sharpness_position(directory: str, fft_height_energy: dict):
    maximum_sharpness_intervall, distance = get_maximum_sharpness_intervall(fft_height_energy)
    epsilon = distance / 4
    # print(maximum_sharpness_intervall)
    points_within_highest_sharpness_intervall = [point for point in fft_height_energy if
                                                 maximum_sharpness_intervall[0] + epsilon < point <
                                                 maximum_sharpness_intervall[
                                                     1] - epsilon]
    point_a = points_within_highest_sharpness_intervall[0]
    val_a = fft_height_energy[point_a]
    point_b = points_within_highest_sharpness_intervall[-1]
    val_b = fft_height_energy[point_b]
    length = len(points_within_highest_sharpness_intervall)
    point_c = points_within_highest_sharpness_intervall[length // 2]
    val_c = fft_height_energy[point_c]

    return find_max_from_3_points(point_a, val_a, point_b, val_b, point_c, val_c)


def returns_blured_mask(matrix, inner_ring, outer_ring):
    kernel = numpy.array([
        [1 / 9, 1 / 9, 1 / 9],
        [1 / 9, 1 / 9, 1 / 9],
        [1 / 9, 1 / 9, 1 / 9]
    ])
    dx, dy = numpy.shape(kernel)

    kx, ky = 7, 7

    shape = matrix.shape

    center_i, center_j = shape[0] // 2, shape[1] // 2

    lines_with_ones = range(center_i - outer_ring, center_i + outer_ring + 1)

    for line in range(center_i - outer_ring):
        for index in range(len(matrix[line])):
            matrix[line][index] = 0

    for line in range(center_i + outer_ring + 1, shape[0]):
        for index in range(len(matrix[line])):
            matrix[line][index] = 0

    for line in lines_with_ones:

        delta_j_outer = int(numpy.sqrt(outer_ring ** 2 - (line - center_i) ** 2))

        if line not in range(center_i - inner_ring, center_i + inner_ring):
            for index in range(center_j - delta_j_outer):
                matrix[line][index] = 0
            for index in range(center_j + delta_j_outer, shape[1]):
                matrix[line][index] = 0

        else:
            delta_j_inner = int(numpy.sqrt(inner_ring ** 2 - (line - center_i) ** 2))
            for index in range(center_j - delta_j_outer):
                matrix[line][index] = 0
            for index in range(center_j - delta_j_inner, center_j + delta_j_inner):
                matrix[line][index] = 0
            for index in range(center_j + delta_j_outer, shape[1]):
                matrix[line][index] = 0

    for x in range(center_j - outer_ring, center_j + outer_ring):  # Blurs the outer shell of the masked image
        y_1 = 2 * center_i + (
                4 * (center_i ** 2) - 4 * (
                center_j ** 2 - 2 * center_j * x + x ** 2 + center_i ** 2 - outer_ring ** 2)) ** (1 / 2)
        y_1 = int(y_1 / 2)
        y_2 = - y_1
        for index_y in range(y_1 - ky, y_1 + ky):
            for index_x in range(x - kx, x + kx):
                matrix[index_y][index_x] = numpy.sum(
                    matrix[index_y:index_y + dy, index_x: index_x + dx] * kernel)
        for index_y in range(y_2 - ky, y_2 + ky):
            for index_x in range(x - kx, x + kx):
                matrix[index_y][index_x] = numpy.sum(
                    matrix[index_y:index_y + dy, index_x: index_x + dx] * kernel)

    return matrix


def sum_fourier_abs(fourier_transformed, inner_ring, outer_ring):
    shape = fourier_transformed.shape
    total = 0

    center_i, center_j = shape[0] // 2, shape[1] // 2

    lines_with_ones = range(center_i - outer_ring, center_i + outer_ring)

    for i in lines_with_ones:
        delta_j_outer = int(numpy.sqrt(outer_ring ** 2 - (i - center_i) ** 2))

        if i not in range(center_i - inner_ring, center_i + inner_ring):
            total += numpy.sum(fourier_transformed[i, center_j - delta_j_outer:center_j + delta_j_outer])

        else:
            delta_j_inner = int(numpy.sqrt(inner_ring ** 2 - (i - center_i) ** 2))
            total += numpy.sum(fourier_transformed[i, center_j - delta_j_outer:center_j - delta_j_inner])
            total += numpy.sum(fourier_transformed[i, center_j + delta_j_inner:center_j + delta_j_outer])
    return total


def main(directory: str):
    list_of_imgs = initialize_list_img(directory)
    fft_height_energy = fft_plot(list_of_imgs)
    max_sharpness_position, quadratic_equation_approximation = get_max_sharpness_position(directory, fft_height_energy)
    # print(max_sharpness_position, quadratic_equation_approximation)

    plt.plot([fft_height_energy[a] for a in fft_height_energy], 'x-')
    plt.xlabel("Slice Number")
    # plt.ylabel(f"FFT energy in r>{rmin} and r<{rmax}")
    plt.show()


if __name__ == '__main__':
    print(return_height_for_sharpest_square(
        'C:\\Code\\github.com\\naeldarw\\birthdayreminder\\EPFL image project\\21\\4863.4074.jpg',
        1,
        'C:\\Code\\github.com\\naeldarw\\birthdayreminder\\EPFL image project\\21\\4871.0274.jpg',
        10, 'C:\\Code\\github.com\\naeldarw\\birthdayreminder\\EPFL image project\\21\\4874.2024.jpg',
        14))
    #main('C:\\Code\\github.com\\naeldarw\\birthdayreminder\\EPFL image project\\21')
    img = image.imread('C:\\Code\\github.com\\naeldarw\\birthdayreminder\\EPFL image project\\21\\4864.2541.jpg')
    im = numpy.array(img).astype(float)
    im = returns_blured_mask(im, 0, 200)

    plt.imshow(im, interpolation='nearest')
    plt.show()

# print(min(fftsum) / max(fftsum) * 100)

# print(right_extremum(100), 'right')
# print(left_extremum(500), 'left')
# fft_plot_dic = fft_plot(list_img)
# print(find_max_from_3_points(478, fft_plot_dic[478], 546, fft_plot_dic[546], 650, fft_plot_dic[650]))
