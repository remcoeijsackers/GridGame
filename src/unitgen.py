import random 

class unitgenerator:

    def get_name(self) -> str:
        first_names = ['John', 'Andy', 'Jack', 'James', 'Amy', 'Misty', 'Charles', 'Wiliam', 'Bill', 'Jennifer', 'Aaron']
        middle_names = ['A.', 'P.', 'M.', 'G.', 'T.', 'M.', 'K.']
        last_names = ['Thompson', 'Jones', 'Baker', 'Ice', 'Tusk', 'Bacon', 'Friday', 'Fisher', 'Jackson', 'Middleton',]

        return "{} {} {}".format(random.choice(first_names), random.choice(middle_names), random.choice(last_names)) 

    def get_image(self) -> str:
        return "assets/user{}.png".format(random.randrange(1,6))
    
    def get_age(self) -> str:
        return "{}".format(random.randrange(20,60))

