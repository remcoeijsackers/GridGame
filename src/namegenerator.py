import random 

class namegen:

    def get_name(self) -> str:
        first_names = ['John', 'Andy', 'Jack', 'James', 'Amy', 'Misty', 'Charles', 'Wiliam', 'Bill', 'Jennifer', 'Aaron']
        middle_names = ['A.', 'P.', 'M.', 'G.', 'T.', 'M.', 'K.']
        last_names = ['Thompson', 'Jones', 'Baker', 'Ice', 'Tusk', 'Bacon', 'Friday', 'Fisher', 'Jackson', 'Middleton',]

        return "{} {} {}".format(random.choice(first_names), random.choice(middle_names), random.choice(last_names)) 
