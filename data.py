import codecs
import numpy as np


class Data_normal():
    def __init__(self, rate=0.8):
        self.rate = rate
        self.train = Dataset()
        self.test = Dataset()

    def get_data(self, filename):
        with codecs.open(filename, 'r') as f:
            import random
            for line in f:
                user, item, rating = line.strip().split()[:3]
                if random.random() < self.rate:
                    self.train.add(user, item, rating)
                else:
                    self.test.add(user, item, rating)


class Data_coldStart():
    def __init__(self, rate=0.9):
        self.rate = rate
        self.train = Dataset()
        self.test = Dataset()

    def read_data(self):
        with open('train.txt') as f:
            for line in f:
                user, item, rating = line.strip().split()
                self.train.add(user, item, rating)

        with open('test.txt') as f:
            for line in f:
                user, item, rating = line.strip().split()
                self.test.add(user, item, rating)

        print('train %d; test %d' % (len(self.train), len(self.test)))
        print('there are %d actors' % self.actor_num)
        print('there are %d countries' % self.countries_num)
        print('there are %d directors' % self.directors_num)
        print('there are %d genres' % self.genres_num)

    def get_data(self, filename):
        users = set()
        items = set()
        ratings = []
        with codecs.open(filename, 'r') as f:
            for line in f.readlines()[1:6000]:
                user, item, rating = line.strip().split()[:3]
                users.add(user)
                items.add(item)
                ratings.append((user, item, rating))
        self.data_cleaning(items)
        import random
        train_items = set()
        test_items = set()
        for item in items:
            if random.random() <= self.rate:
                train_items.add(item)
            else:
                test_items.add(item)
        for user, item, rating in ratings:
            if item in train_items:
                self.train.add(user, item, rating)
            elif item in test_items:
                self.test.add(user, item, rating)

        with open('train.txt', 'w') as f:
            for line in self.train.ratings:
                f.writelines('\t'.join([str(elem) for elem in line]) + '\n')
        with open('test.txt', 'w') as f:
            for line in self.test.ratings:
                f.writelines('\t'.join([str(elem) for elem in line]) + '\n')

        print('train %d; test %d'%(len(self.train), len(self.test)))
        print('there are %d actors'%self.actor_num)
        print('there are %d countries'%self.countries_num)
        print('there are %d directors'%self.directors_num)
        print('there are %d genres'%self.genres_num)

    def data_cleaning(self, items):
        if not (len(self.item_actors) and\
            len(self.item_country) and\
            len(self.item_director) and\
                len(self.item_genres)):
            print('error check Front-end work item_actors %d;item_country %d;item_director %d;item_genres %d'%
                  (len(self.item_actors), len(self.item_country), len(self.item_director), len(self.item_genres)))
            exit(-1)
        del_items = set()
        for item in items:
            if item not in self.item_actors or\
                item not in self.item_country or\
                item not in self.item_director or\
                    item not in self.item_genres:
                del_items.add(item)
        items -= del_items

    def get_actor(self, filename, weight=10):
        """
        :param filename:文件名字
        :param weight: 只选择不小于weight的actor
        """
        item_actor_list = []
        actors_counts = {}
        with codecs.open(filename, 'r', "ISO-8859-1") as f:
            for line in f.readlines()[1:]:
                item, actor = line.strip().split()[:2]
                if actor not in actors_counts:
                    actors_counts[actor] = 0
                item_actor_list.append((item, actor))
                actors_counts[actor] += 1

        self.actors = {}
        for actor, count in actors_counts.items():
            if count >= weight:
                self.actors[actor] = len(self.actors)
        self.actor_num = len(self.actors)
        self.item_actors = {}
        for item, actor in item_actor_list:
            if actor in self.actors:
                if item not in self.item_actors:
                    self.item_actors[item] = np.zeros(shape=self.actor_num)
                self.item_actors[item][self.actors[actor]] = 1
                flag = 1

    def get_country(self, filename):
        self.countries = {}
        item_countries_list = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f.readlines()[1:]:
                try:
                    item, country = line.strip().split()
                except BaseException:
                    item = line.strip()
                    country = 'UNK'
                if country not in self.countries:
                    self.countries[country] = len(self.countries)
                item_countries_list.append((item, country))
        self.countries_num = len(self.countries)
        self.item_country = {}
        for item, country in item_countries_list:
            if item not in self.item_country:
                self.item_country[item] = np.zeros(shape=self.countries_num)
            self.item_country[item][self.countries[country]] = 1

    def get_director(self, filename):
        self.directors = {}
        item_directors_list = []
        with open(filename, 'r', encoding='ISO-8859-1') as f:
            for line in f.readlines()[1:]:
                item, director = line.strip().split()[:2]
                if director not in self.directors:
                    self.directors[director] = len(self.directors)
                item_directors_list.append((item, director))
        self.directors_num = len(self.directors)
        self.item_director = {}
        for item, country in item_directors_list:
            if item not in self.item_director:
                self.item_director[item] = np.zeros(shape=self.directors_num)
            self.item_director[item][self.directors[director]] = 1

    def get_genres(self, filename, weight=20):
        genres_count = {}
        item_genres_list = []
        with open(filename, 'r') as f:
            for line in f.readlines()[1:]:
                item, genre = line.strip().split()
                if genre not in genres_count:
                    genres_count[genre] = 0
                genres_count[genre] += 1
                item_genres_list.append((item, genre))
        self.genres = {}
        for genre, count in genres_count.items():
            if count > weight:
                self.genres[genre] = len(self.genres)
        self.genres_num = len(self.genres)
        self.item_genres = {}
        for item, genre in item_genres_list:
            if genre in self.genres:
                if item not in self.item_genres:
                    self.item_genres[item] = np.zeros(self.genres_num)
                self.item_genres[item][self.genres[genre]] = 1

    def size(self):
        return self.actor_num, self.countries_num, self.directors_num,self.genres_num


class Dataset():
    def __init__(self):
        self.users = set()
        self.items = set()
        self.ratings = []

    def add(self, user, item, rating):
        self.users.add(user)
        self.items.add(item)
        self.ratings.append((user, item, float(rating)))

    def __len__(self):
        return len(self.ratings)



