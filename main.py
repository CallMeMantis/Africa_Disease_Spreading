from PIL import Image
from scipy.misc import imsave
import numpy
import random as rd


def get_disease_probability(rgb_data):
    probability_data = []
    for i, y in enumerate(rgb_data):
        probability_data.append([])
        for x in y:
            # print(x[0])
            prob = x[0]/255
            if prob == 1.0:
                prob = 0
            probability_data[i].append(prob)
    return probability_data


def get_rgba(image_name):
    im = Image.open(str(image_name))
    rgb_im = im.convert('LA')
    # rgb_im = rgb_im.save('testing.png')
    rgb_data = []
    pix = rgb_im.load()
    for x in range(im.size[0]):
        rgb_data.append([])
        for y in range(im.size[1]):
            rgb_data[x].append(pix[x,y])
    return rgb_data


class Disease:

    def __init__(self, filename):

        self.filename = filename
        self.rgb_data = get_rgba(self.filename)
        self.prob = get_disease_probability(self.rgb_data)
        self.map = []
        self.sizex = len(self.prob)
        self.sizey = len(self.prob[0])
        self.population = self.sizex * self.sizey
        self.sick_person_position_row = []
        self.sick_person_position_col = []
        self.population = self.sizex * self.sizey
        self.infected_people_amount = 100
        self.time = 0
        self.time_limit = 100

    def create_map(self):
        for i in range(self.sizex):
            self.map.append([])
            for j in range(self.sizey):
                self.map[i].append(0)

    def create_population(self):

        while self.infected_people_amount >= 0:
            row = rd.randint(0, self.sizex - 1)
            col = rd.randint(0, self.sizey - 1)
            if self.map[row][col] == 0:
                self.map[row][col] = 1
                self.infected_people_amount -= 1

        # not infected people
        for i in range(self.population):
            row = rd.randint(0, self.sizex - 1)
            col = rd.randint(0, self.sizey - 1)
            if self.map[row][col] == 0:
                self.map[row][col] = 2

    def disease_transmission(self, i, j):

        self.map[i][j] = 1

        try:
            if self.map[i - 1][j - 1] == 2:
                self.map[i - 1][j - 1] = 1
        except IndexError:
            pass

        try:
            if self.map[i - 1][j] == 2:
                self.map[i - 1][j] = 1
        except IndexError:
            pass

        try:
            if self.map[i - 1][j + 1] == 2:
                self.map[i - 1][j + 1] = 1
        except IndexError:
            pass

        try:
            if self.map[i][j - 1] == 2:
                self.map[i][j - 1] = 1
        except IndexError:
            pass

        try:
            if self.map[i][j + 1] == 2:
                self.map[i][j + 1] = 1
        except IndexError:
            pass

        try:
            if self.map[i + 1][j - 1] == 2:
                self.map[i + 1][j - 1] = 1
        except IndexError:
            pass

        try:
            if self.map[i + 1][j] == 2:
                self.map[i + 1][j] = 1
        except IndexError:
            pass

        try:
            if self.map[i + 1][j + 1] == 2:
                self.map[i + 1][j + 1] = 1
        except IndexError:
            pass

    def spread_disease(self):

        for i in range(self.sizex):
            for j in range(self.sizey):
                if self.map[i][j] == 1:
                    self.sick_person_position_row.append(i)
                    self.sick_person_position_col.append(j)

        for i in range(len(self.sick_person_position_row)):
            self.transm_prob = numpy.random.rand()
            # print(self.transm_prob)
            if self.transm_prob < self.prob[self.sick_person_position_row[i]][self.sick_person_position_col[i]]:
                Disease.disease_transmission(self, self.sick_person_position_row[i],
                                             self.sick_person_position_col[i])

    def save_png(self, time, map):

        # im = Image.open(str(self.filename))
        # rgb_im = im.convert('RGB')
        # # rgb_im = rgb_im.save('testing.png')
        # rgb_data = []
        # pix = rgb_im.load()
        # for x in range(im.size[0]):
        #     rgb_data.append([])
        #     for y in range(im.size[1]):
        #         rgb_data[x].append(pix[x, y])

        time = str(self.time)
        name = 'disease_fire_' + time + ".png"
        name = str(name)
        imsave(name, self.map)

        im = Image.open(name)
        im = im.rotate(-90)
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        im.save(name)

    def main(self):
        Disease.create_map(self)
        Disease.create_population(self)
        while self.time <= self.time_limit:
            Disease.save_png(self, self.time, self.map)
            Disease.spread_disease(self)
            self.time += 1

            # for i in range(len(self.map)):
            #     print(self.map[i])
            # print()

# rgb_data = get_rgba("main.jpg")
# print(get_disease_probability(rgb_data))

disease = Disease("main2.jpg")
disease.main()