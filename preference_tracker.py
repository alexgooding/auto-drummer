import errno
import os
import ast
from operator import itemgetter
from random import choices

from tinydb import TinyDB, Query
from tinydb.operations import set as tinydb_set
from tinydb.operations import increment

# Add like/dislike counter for use in learning algorithm.

class Tracker:
    try:
        os.makedirs(os.getenv('LOCALAPPDATA') + r'\AutoDrummer')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    user_preferences = TinyDB(os.getenv('LOCALAPPDATA') + r'\AutoDrummer\UserPreferences.json')
    # Create like/dislike counter.
    if len(user_preferences) == 0:
        user_preferences.insert({'rating_counter': 0})

    def get_rating_counter(self):
        User = Query()
        return self.user_preferences.search(User['rating_counter'])[0]['rating_counter']

    def calculate_rating(self, rating, preference):
        if preference:
            rating += 1
        else:
            rating -= rating/10

        return rating

    def assign_rating(self, key, rating):
        User = Query()
        self.user_preferences.update(tinydb_set('rating', rating), User.id == key)
        self.user_preferences.update(increment('rating_counter'), User.rating_counter >= 0)

    def create_entry(self, key):
        self.user_preferences.insert({'id': key, 'rating': 1})

    def search_preferences(self, key):
        User = Query()
        if self.user_preferences.get(User.id == key) == None:
            self.create_entry(key)
        return self.user_preferences.get(User.id == key)['rating']

    def condense_pattern(self, hit):
        while hit[1] > 16:
            hit[1] -= 16
        return hit

    # Normalise sorted data to between 0 and 1.
    def normalise_data(self, sorted_data):
        max = sorted_data[0]['rating']
        min = sorted_data[-1]['rating']
        for element in sorted_data:
            element['rating'] = (element['rating']-min)/(max-min)
        return sorted_data

    # Convert data between 0 and 1 to weights.
    def convert_to_weights(self, data):
        sum_of_data = sum([x['rating'] for x in data])
        for element in data:
            element['rating'] = element['rating']/sum_of_data
        return data

    def sort_data(self):
        return sorted(self.user_preferences.all(), key=itemgetter('rating'), reverse=True)

    def retrieve_n_highest_rated(self, n):
        sorted_hits = self.sort_data()
        return [ast.literal_eval(hit['id']) for hit in sorted_hits[0:n]]

    def sample_n_hits(self, n, pattern_length):
        User = Query()
        relevant_data = [element for element in self.user_preferences.search(User.id.exists()) if int(ast.literal_eval(element['id'])[1]) <= pattern_length*16]
        hit_weights = self.convert_to_weights(relevant_data)
        population = [ast.literal_eval(element['id']) for element in hit_weights]
        weights = [element['rating'] for element in hit_weights]
        # Use a set to sample to avoid duplicates.
        sampled_hits = set()
        sample_counter = 0
        while len(sampled_hits) < n and sample_counter < n*10:
            sampled_hits.add(tuple(choices(population, weights)[0]))
            sample_counter += 1
        sampled_hits = list(sampled_hits)

        return sampled_hits

