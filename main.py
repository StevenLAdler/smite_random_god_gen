from bs4 import BeautifulSoup as bs
import requests
from random import choice

class GodPicker():

    def __init__(self, verbose=True):
        self.verbose = verbose

    def get_god_details(self):
        URL = "https://smite.fandom.com/wiki/List_of_gods"
        r = requests.get(URL)
        soup = bs(r.content, features="html5lib")
        gods = [god for god in soup.find_all("tr")[1:]]
        god_details = []

        for god in gods:
            try:
                god_details.append(tuple([str(god.findChildren(recursive=False)[i]).split("title=")[1].split('"')[1] for i in range (1,6)]))
            except(IndexError):
                break
        
        self.gods = god_details

    def sort_cat_data(self):
        cat_data = {'pantheon':{},
                    'attack_type':{},
                    'power_type':{},
                    'class':{}}
        god_list = []
        
        for god in self.gods:
            cat_data['pantheon'].setdefault(god[1], []).append(god[0])
            cat_data['attack_type'].setdefault(god[2], []).append(god[0])
            cat_data['power_type'].setdefault(god[3], []).append(god[0])
            cat_data['class'].setdefault(god[4], []).append(god[0])

            god_list.append(god[0])

        self.cat_data = cat_data
        self.god_list = god_list

    def get_attr(self):
        attr = []
        for key in self.cat_data.keys():
            attr.append([key for key in self.cat_data[key].keys()])
        
        self.attr = attr

    def get_query(self):
        if self.verbose:
            print("Attributes:")
            [print(attr) for attr in self.attr]
            print("Enter a comma seperated list of attributes to randomize on, blank for random god")
            options = input("ex: Greek, Melee\n")
        else:
            options = input("Enter comma seperated list of attributes, blank for random god\n")
        if options != '':
            self.options  = [option.strip().capitalize() for option in options.split(',')]
        else:
            self.options = None

    def get_possible_gods(self):
        cat_data = self.cat_data
        god_lists = []

        if not self.options:
            self.possible_gods = self.god_list
            return

        for key in cat_data.keys():
            for option in self.options:
                if option in cat_data[key]:
                    god_lists.append(cat_data[key][option])
        self.possible_gods = (set.intersection(*map(set,god_lists)))

    def get_rand_god(self):
        print(choice(list(self.possible_gods)))
            

if __name__ == "__main__":
    gp = GodPicker(verbose=True)
    gp.get_god_details()
    gp.sort_cat_data()
    gp.get_attr()

    gp.get_query()
    gp.get_possible_gods()
    gp.get_rand_god()
