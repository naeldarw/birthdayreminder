import time
import numpy
import os
# import tifffile
import matplotlib.pyplot as plt
import imageio
import shutil
import matplotlib.image as image


class JpgFilesToHeight:
    def __init__(self, directory: str, fft_square: str, fft_whole_img: str):
        self.height_to_focus_number = {}
        band_square = find_band(80, 70, 1440, 1920, 0, 0)
        band = find_band(600, 450, 1440, 1920, 0, 0)
        band_prime = find_band(200, 50, 1440, 1920, 0, 0)  # We play with the frequencies that we want to keep
        for i, im in enumerate(os.listdir(fft_whole_img)[540:610]):
            height = float(os.path.splitext(im)[0])
            print(i, height)

            img = imageio.v2.imread(os.path.join(directory, str(height) + '.jpg'))
            img = numpy.array(img).astype(float)
            disks_energy = self.return_disks_energy(img, 8, numpy.array([632.2, 452.6]),
                                                    numpy.array([17.5, -8.7]), numpy.array([8.7, 17.5]), 20)
            # (632.2, 452.6) is the coordinate of the top left disk ; (17.5, -8.7) is the vector to go to the next left
            # disk ; (8.7, 17.5) is the vector to go to the nearest disk underneath; (20) ** 2 is the number of disks
            # we take the sum of. All measured by hand.

            '''img = returns_masked_matrix(img, 0, 180, 530, 853), (530, 853) is the center of the well, measured by hand
            180 is the radius of the well(a disk), measured by hand
            boss_value = img_boss_value(img)'''

            fft_img_square = imageio.v2.imread(os.path.join(fft_square, im))
            fft_img_square = numpy.array(fft_img_square).astype(float)
            fft_whole_im = imageio.v2.imread(os.path.join(fft_whole_img, im))
            fft_whole_im = numpy.array(fft_whole_im).astype(float)

            fft_energy_square = numpy.abs(fft_img_square[band_square]).sum()
            fft_energy_whole_img = numpy.abs(fft_whole_im[band]).sum()
            fft_energy_whole_img_prime = numpy.abs(fft_whole_im[band_prime]).sum()

            self.height_to_focus_number[height] = fft_energy_whole_img * 2 + \
                                                  (fft_energy_square + 50 * disks_energy) * 13 + \
                                                  fft_energy_whole_img_prime
        self.valid_heights = list(self.height_to_focus_number.keys())
        self.valid_heights = [height for i, height in enumerate(self.valid_heights[:len(self.valid_heights) - 1]) if
                              not 2 * self.height_to_focus_number[height] < self.height_to_focus_number[
                                  self.valid_heights[i + 1]]]
        self.valid_heights.sort()
        print(self.valid_heights)
        self.valid_focus_numbers = [self.height_to_focus_number[key] for key in self.valid_heights]
        print(self.height_to_focus_number)
        plt.plot(self.valid_heights, self.valid_focus_numbers)
        plt.show()

    @staticmethod
    def find_bounded_int_in_sorted_list(sorted_lis: list, val_to_fit: float):
        idx = 1
        while not sorted_lis[idx - 1] < val_to_fit < sorted_lis[idx + 1]:
            idx += 1
        if abs(val_to_fit - sorted_lis[idx - 1]) < abs(val_to_fit - sorted_lis[idx + 1]):
            return sorted_lis[idx - 1]
        else:
            return sorted_lis[idx + 1]

    def return_sharpest_height_for_square(self, current_height: float, epsilon: float) -> int:
        pic1_height = self.find_bounded_int_in_sorted_list(self.valid_heights, current_height)
        pic1_focus = self.height_to_focus_number[pic1_height]
        pic2_height = self.find_bounded_int_in_sorted_list(self.valid_heights, current_height - epsilon)
        pic2_focus = self.height_to_focus_number[pic2_height]
        pic3_height = self.find_bounded_int_in_sorted_list(self.valid_heights, current_height + epsilon)
        pic3_focus = self.height_to_focus_number[pic3_height]
        return self.find_max_from_3_points(pic1_height, pic1_focus, pic2_height, pic2_focus, pic3_height, pic3_focus)[0]

    def test_matrix_height_vs_epsilon(self, sharpest_height_square: float, delta_height=10,
                                      max_epsilon=10,
                                      precision_unit=10):
        """Test the return_sharpest_height function for heights from sharpest_height_square - delta_height to
        sharpest_height_square + delta_height and for epsilons from - max_epsilon to max_epsilon"""
        x, y = max_epsilon * precision_unit, delta_height * 2 * precision_unit
        matrix = numpy.zeros((x, y))
        for i in range(x):
            for j in range(- delta_height * precision_unit, delta_height * precision_unit):
                sharpest_height_measured = self.return_sharpest_height_for_square(sharpest_height_square + j / 10, i / 10)
                matrix[i][j + delta_height * precision_unit] = abs(sharpest_height_measured - sharpest_height_square)
        plt.imshow(matrix)
        plt.show()
        return matrix

    @staticmethod
    def find_max_from_3_points(x_1, y_1, x_2, y_2, x_3, y_3):
        """return the x local maximum's position of the quadratic"""
        quadratic = numpy.polyfit((x_1, x_2, x_3), (y_1, y_2, y_3), deg=2)
        a = quadratic[0]
        b = quadratic[1]
        c = quadratic[2]

        x = -b / (2 * a)

        return x, (a, b, c)

    @staticmethod
    def sum_fourier_square_abs(fourier_transformed, inner_ring, outer_ring, center_i, center_j):
        """Returns the sum of the pixel within the band defined by (center_i, center_j), inner_ring and outer_ring."""
        total = 0

        lines_with_ones = range(int(numpy.ceil(center_i)) - outer_ring, int(numpy.floor(center_i)) + outer_ring)

        for i in lines_with_ones:
            delta_j_outer = int(numpy.sqrt(outer_ring ** 2 - (i - center_i) ** 2))

            if i not in range(int(numpy.ceil(center_i)) - inner_ring, int(numpy.floor(center_i)) + inner_ring):
                total += numpy.sum(
                    fourier_transformed[i, round(center_j) - delta_j_outer:round(center_j) + delta_j_outer])

            else:
                delta_j_inner = int(numpy.sqrt(inner_ring ** 2 - (i - center_i) ** 2))
                total += numpy.sum(
                    fourier_transformed[i, round(center_j) - delta_j_outer:round(center_j) - delta_j_inner])
                total += numpy.sum(
                    fourier_transformed[i, round(center_j) + delta_j_inner:round(center_j) + delta_j_outer])
        return total

    def return_disks_energy(self, img, radius: float, top_left, step_right, step_down,
                            side_length: int):  # radius is the radius of a disk
        centers_disks = render_center_disks_of_square(top_left, step_right, step_down, side_length)
        total = 0
        for center in centers_disks:
            total += self.sum_fourier_square_abs(img, 0, radius, center[1], center[0])
        return total


def returns_fft_energy_for_img(img, band):
    energy = numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(img)))[band].sum()
    return energy


def returns_masked_matrix(matrix, inner_ring, outer_ring, center_i, center_j):  # center_i in the y position, and
    # center_j in the x position
    shape = matrix.shape

    lines_to_handel = range(center_i - outer_ring, center_i + outer_ring + 1)

    for line in range(center_i - outer_ring):
        for pixel in range(len(matrix[line])):
            matrix[line][pixel] = 0

    for line in range(center_i + outer_ring + 1, shape[0]):
        for pixel in range(len(matrix[line])):
            matrix[line][pixel] = 0

    for line in lines_to_handel:

        delta_j_outer = int(numpy.sqrt(outer_ring ** 2 - (line - center_i) ** 2))

        if line not in range(center_i - inner_ring, center_i + inner_ring):
            for pixel in range(center_j - delta_j_outer):
                matrix[line][pixel] = 0
            for pixel in range(center_j + delta_j_outer, shape[1]):
                matrix[line][pixel] = 0

        else:
            delta_j_inner = int(numpy.sqrt(inner_ring ** 2 - (line - center_i) ** 2))
            for pixel in range(center_j - delta_j_outer):
                matrix[line][pixel] = 0
            for pixel in range(center_j - delta_j_inner, center_j + delta_j_inner):
                matrix[line][pixel] = 0
            for pixel in range(center_j + delta_j_outer, shape[1]):
                matrix[line][pixel] = 0

    return matrix


def render_center_disks_of_square(top_left, step_right, step_down,
                                  side_length: int) -> list:  # These are measured by hand(top_left(632.2, 452.6),
    # step_right(17.4, -8.6),
    # side_length(20)), side_length is the number of disks per side
    disks_centers = []
    top_left -= step_down
    for _ in range(side_length):
        top_left += step_down
        for j in enumerate(range(side_length)):
            center = top_left + j * step_right
            disks_centers.append(tuple(center))
    return disks_centers


def find_band(rmax: int, rmin: int, x: int, y: int, a: int, b: int):  # (a, b) is the center of the band
    coords = numpy.mgrid[0:x, 0:y]
    coords = coords.astype(float)
    coords[0] -= x / 2
    coords[1] -= y / 2
    coords[0] += b
    coords[1] -= a
    r = numpy.sqrt(coords[0] ** 2 + coords[1] ** 2)
    band = numpy.logical_and(r > rmin, r < rmax)
    return band


def img_boss_value(matrix):
    return numpy.sum(matrix > matrix.mean())


'''def mean_value(matrix, shape):
    s = numpy.sum(matrix)
    if type(shape) == tuple:
        x, y = shape
        return s / (x * y)
    else:
        print(shape)
        area = numpy.pi * (shape ** 2)
        return s / area

def image_boss(matrix):
    mean = matrix.mean()
    print(mean)
    x, y = matrix.shape
    for i in range(x):
        for j in range(y):
            if matrix[i][j] > mean:
                matrix[i][j] = 0
            else:
                matrix[i][j] = 255
    # plt.imshow(matrix)
    # plt.show()

    return matrix'''


def main():
    jpg_files_to_int_height = JpgFilesToHeight('21', 'fft_square', 'fft_of_whole_images')
    jpg_files_to_int_height.test_matrix_height_vs_epsilon(4860.21)


if __name__ == '__main__':
    main()
