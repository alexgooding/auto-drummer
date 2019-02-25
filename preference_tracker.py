## Copyright (C) 2019 Alex Gooding

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.

import errno
import os
import ast
from operator import itemgetter
from random import choices

from tinydb import TinyDB, Query
from tinydb.operations import set as tinydb_set
from tinydb.operations import increment

"""
The ``preference_tracker`` module
======================

Use it to import a Tracker object.
Once imported, a tracker can be instantiated to create/locate a local database that will store
the users hit preferences when using the Auto Drummer app.

:Example:

>>> from preference_tracker import Tracker
"""

class Tracker:
    # Create/locate the user preference database.
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
        """
        Retrieves how many ratings have been logged.

        :return: returns the number of ratings that have been logged as an integer.
        """
        User = Query()
        return self.user_preferences.search(User['rating_counter'])[0]['rating_counter']

    def calculate_rating(self, rating, preference):
        """
        Calculates the new value of a rating based on a preference.

        :param rating: the rating to be updated.
        :param preference: the preference being applied expressed as a boolean (True=like, False=dislike).
        :return: returns the updated rating.
        """
        if preference:
            rating += 1
        else:
            rating -= rating/10

        return rating

    def assign_rating(self, key, rating):
        """
        Assigns rating to the key provided.

        :param key: the hit in the database that is to be updated.
        :param rating: the rating that the hit will be updated with.
        :return: returns nothing.
        """
        User = Query()
        self.user_preferences.update(tinydb_set('rating', rating), User.id == key)
        self.user_preferences.update(increment('rating_counter'), User.rating_counter >= 0)

    def create_entry(self, key):
        """
        Creates an entry in database with the key provided and default rating 1.

        :param key: the key to be added to the database.
        :return: returns nothing.
        """
        self.user_preferences.insert({'id': key, 'rating': 1})

    def search_preferences(self, key):
        """
        Retrieves the rating corresponding to a particular key.

        :param key: the key that is to be searched for.
        :return: returns the rating corresponding to the particular key.
        """
        User = Query()
        if self.user_preferences.get(User.id == key) == None:
            self.create_entry(key)
        return self.user_preferences.get(User.id == key)['rating']

    def condense_hit(self, hit):
        """
        Condenses any timing of hit into its one bar equivalent position.

        :param hit: the hit to be condensed.
        :return: returns the condensed hit.
        """
        while hit[1] > 16:
            hit[1] -= 16
        return hit

    def normalise_data(self, sorted_data):
        """
        Normalises sorted data ratings to between 0 and 1.

        :param sorted_data: the sorted data to be normalised.
        :return: returns the normalised data.
        """
        max = sorted_data[0]['rating']
        min = sorted_data[-1]['rating']
        for element in sorted_data:
            element['rating'] = (element['rating']-min)/(max-min)
        return sorted_data

    # Convert data between 0 and 1 to weights.
    def convert_to_weights(self, data):
        """
        Converts data ratings into weights between 0 and 1.

        :param data: the data to be converted.
        :return: returns the data with the ratings converted into weights.
        """
        sum_of_data = sum([x['rating'] for x in data])
        for element in data:
            element['rating'] = element['rating']/sum_of_data
        return data

    def sort_data(self):
        """
        Sorts the whole database by rating in descending order.

        :return: returns the sorted data.
        """
        return sorted(self.user_preferences.all(), key=itemgetter('rating'), reverse=True)

    def sample_n_hits(self, n, pattern_length):
        """
        Samples n hits from the database based on the current ratings converted into weights.

        :param n: the number of hits to be sampled.
        :param pattern_length: the length of the pattern to be sampled.
        :return: returns the sampled hits as a list.
        """
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

