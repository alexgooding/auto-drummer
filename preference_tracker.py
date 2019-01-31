from tinydb import TinyDB, Query
from tinydb.operations import set
import os, errno


class Tracker:
    try:
        os.makedirs(os.getenv('LOCALAPPDATA') + r'\AutoDrummer')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    user_preferences = TinyDB(os.getenv('LOCALAPPDATA') + r'\AutoDrummer\UserPreferences.json')

    def calculate_rating(self, rating, preference):
        if preference:
            rating += rating / 10
        else:
            rating -= rating / 10

        return rating

    def assign_rating(self, key, rating):
        User = Query()
        self.user_preferences.update(set('rating', rating), User.id == key)

    def create_entry(self, key):
        self.user_preferences.insert({'id' : key, 'rating' : 1})

    def search_preferences(self, key):
        User = Query()
        return self.user_preferences.get(User.id == key)['rating']

