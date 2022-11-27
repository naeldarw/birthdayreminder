import numpy
import os
# import tifffile
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import matplotlib.image as image


# directory = 'C:\\Code\\github.com\\naeldarw\\birthdayreminder\\EPFL image project\\21'


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
    #print(a, b, c)
    print(x, 'x axis position of the maximum sharpness image')

    return x, (a, b, c)


def find_band():
    img0 = list_img[0]
    img1 = image.imread(img0)
    im = numpy.array(img1).astype(float)
    x, y = im.shape
    max_num = ((x / 2) ** 2 + (y / 2) ** 2) ** (1 / 2)
    min_num = 0
    rmax = max_num - 100
    rmin = min_num + 50
    coords = numpy.mgrid[0:x, 0:y]
    coords = coords.astype(float)
    coords[0] -= x / 2
    coords[1] -= y / 2
    r = numpy.sqrt(coords[0] ** 2 + coords[1] ** 2)
    band = numpy.logical_and(r > rmin, r < rmax)
    return band


def fft_plot(list_im: list) -> dict:
    height_energy = {}
    for i, img in enumerate(list_im):
        #print(i)
        img = image.imread(img)
        im = numpy.array(img).astype(float)
        # im -= numpy.median(im, axis=(0))
        # height_energy[i] = numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(im)))[band].sum()
        height_energy[i] = numpy.max(im) - numpy.min(im) # Method that isn't correct but plots a graph similar to the
        # fft graph
    return height_energy


def initialize_list_img(directory: str):
    list_of_imgs = []  # paths of the images

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        list_of_imgs.append(f)
    return list_of_imgs


def get_maximum_sharpness_intervall(fft_height_energy: dict):  # the images are in "directory"

    # band = find_band()  # We assume that all of the images have the same sizes

    height, energy = max([(height, energy) for height, energy in fft_height_energy.items()], key=lambda a: a[1])
    #print(height, energy, 'height-energy')

    nearest_right_side_local_extremum = right_extremum(height, fft_height_energy)
    nearest_left_side_local_extremum = left_extremum(height, fft_height_energy)

    maximum_sharpness_intervall = (nearest_left_side_local_extremum, nearest_right_side_local_extremum)
    distance = nearest_right_side_local_extremum - nearest_left_side_local_extremum

    return maximum_sharpness_intervall, distance


def get_max_sharpness_position(directory: str, fft_height_energy: dict):
    maximum_sharpness_intervall, distance = get_maximum_sharpness_intervall(fft_height_energy)
    #print(maximum_sharpness_intervall)
    points_within_highest_sharpness_intervall = [point for point in fft_height_energy if
                                                 maximum_sharpness_intervall[0] < point < maximum_sharpness_intervall[
                                                     1]]
    point_a = points_within_highest_sharpness_intervall[0]
    val_a = fft_height_energy[point_a]
    point_b = points_within_highest_sharpness_intervall[-1]
    val_b = fft_height_energy[point_b]
    length = len(points_within_highest_sharpness_intervall)
    point_c = points_within_highest_sharpness_intervall[length // 2]
    val_c = fft_height_energy[point_c]

    return find_max_from_3_points(point_a, val_a, point_b, val_b, point_c, val_c)


def main(directory: str):
    list_of_imgs = initialize_list_img(directory)
    fft_height_energy = fft_plot(list_of_imgs)
    max_sharpness_position, quadratic_equation_approximation = get_max_sharpness_position(directory, fft_height_energy)
    #print(max_sharpness_position, quadratic_equation_approximation)

    plt.plot([fft_height_energy[a] for a in fft_height_energy], 'x-')
    plt.xlabel("Slice Number")
    # plt.ylabel(f"FFT energy in r>{rmin} and r<{rmax}")
    plt.show()


if __name__ == '__main__':
    main('C:\\Code\\github.com\\naeldarw\\birthdayreminder\\EPFL image project\\21')

# print(min(fftsum) / max(fftsum) * 100)

# print(right_extremum(100), 'right')
# print(left_extremum(500), 'left')
# fft_plot_dic = fft_plot(list_img)
# print(find_max_from_3_points(478, fft_plot_dic[478], 546, fft_plot_dic[546], 650, fft_plot_dic[650]))
