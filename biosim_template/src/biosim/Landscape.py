import random

from .Animal import Herbivore, Carnivore

'''Super Class for the Landscape'''


class Landscape:

    @classmethod
    def food_params(cls, param):
        for key, value in param.items():
            if key == 'f_max':
                cls.f_max = value
            else:
                raise KeyError(f'Invalid parameter name: {key}')

    def pop_animals(self, pop):
        """

        Parameters
        ----------
        pop : list With Herbivore

        """
        for animal in pop:
            if animal['species'] == 'Herbivore':
                self.herbivores.append(Herbivore(animal['age'], animal['weight']))
            elif animal['species'] == 'Carnivore':
                self.carnivores.append(Carnivore(animal['age'], animal['weight']))

    def num_herbivores(self):
        """Finds the number of herbivores"""
        return len(self.herbivores)

    def num_carnivores(self):
        """Finds the number of carnivores"""
        return len(self.carnivores)

    def feeding(self):
        """Feeds the herbivores in the landscape"""
        self.fodder = self.f_max
        self.herbivores = sorted(self.herbivores, key=lambda x: x.fitness(), reverse=True)  # Sort herbivores by fitness
        for herbi in self.herbivores:
            if self.fodder >= herbi.params['F']:
                self.fodder -= herbi.params['F']
                herbi.add_weight(herbi.params['F'])
            elif self.fodder == 0:  # The herbivores dont get food, because there are no food left
                break
            else:  # If there are less food then a herbivore can eat
                herbi.add_weight(self.fodder)  # the herbivore get the rest of the food
                self.fodder = 0

    def carnivore_feeding(self):

        self.herbivores = sorted(self.herbivores, key=lambda x: x.fitness())
        for carni in self.carnivores:
            alive_herbivores = self.herbivores
            Hunger = carni.params['F']
            for herbi in alive_herbivores:
                if (carni.fitness()-herbi.fitness())/carni.params['DeltaPhiMax'] > random.random():
                    if herbi.weight > Hunger:
                        carni.add_weight(Hunger)
                        self.herbivores.remove(herbi)
                        break
                    else:
                        carni.add_weight(herbi.weight)
                        self.herbivores.remove(herbi)

    def reproduction(self):
        """Checks hoe many new babies there are and add them to the landscape"""

        self.herbivores.extend([Herbivore(0, bw) for herbi in self.herbivores
                                if (bw := herbi.birth(self.num_herbivores())) > 0])
        # Adds the new babies to the list of herbivores
        self.carnivores.extend([Carnivore(0, bw) for carni in self.carnivores
                                if (bw := carni.birth(self.num_carnivores())) > 0])
        # Adds the new babies to the list of carnivores

    def aging(self):
        """Makes all the animals one year older"""
        for herbi in self.herbivores:
            herbi.year()
        for carni in self.carnivores:
            carni.year()

    def loss_of_weight(self):
        """Removes the weight the animals loses in a year"""
        for herbi in self.herbivores:
            herbi.lose_weight()
        for carni in self.carnivores:
            carni.lose_weight()

    def pop_reduction(self):
        """Removes all animals that dies"""
        alive_herbi = [herbi for herbi in self.herbivores if not herbi.death()]
        self.herbivores = alive_herbi

        alive_carni = [carni for carni in self.carnivores if not carni.death()]
        self.carnivores = alive_carni


class Water(Landscape):
    """Water without food and animals"""

    def __init__(self):
        self.herbivores = []
        self.carnivores = []
        self.fodder = 0  # How much food there are in the Water


class Lowland(Landscape):
    """Lowland with food and animals"""
    f_max = 800

    def __init__(self, herbivores=None, carnivores=None):
        self.herbivores = herbivores if herbivores is not None else []  # Empty list if no list are given
        self.carnivores = carnivores if carnivores is not None else []  # Empty list if no list are given
        self.fodder = self.f_max       # How much food there are in the lowland


class Highland(Landscape):
    """Highland with food and animals"""
    f_max = 300

    def __init__(self, herbivores=None, carnivores=None):
        self.herbivores = herbivores if herbivores is not None else []  # Empty list if no list are given
        self.carnivores = carnivores if carnivores is not None else []  # Empty list if no list are given
        self.fodder = self.f_max  # How much food there are in the Highland


class Dessert(Landscape):
    """Dessert animals and no food"""
    f_max = 0

    def __init__(self, herbivores=None, carnivores=None):
        self.herbivores = herbivores if herbivores is not None else []  # Empty list if no list are given
        self.carnivores = carnivores if carnivores is not None else []  # Empty list if no list are given
        self.fodder = self.f_max  # How much food there are in the Dessert
