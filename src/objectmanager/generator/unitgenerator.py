import random 


def get_name() -> str:
    first_names = ['John', 'Andy', 'Jack', 'James', 'Amy', 'Misty', 'Charles', 'Wiliam', 'Bill', 'Jennifer', 'Aaron', 'Mr.', 'Ms.', 'Dr.']
    middle_names = ['A.', 'P.', 'M.', 'G.', 'T.', 'M.', 'K.', 'L.', 'O.', 'B.', 'C.', 'D.']
    return "{} {}".format(random.choice(first_names), random.choice(middle_names)) 
    
def get_image() -> str:
    return "assets/user{}.png".format(random.randrange(1,6))

def get_age() -> str:
    return "{}".format(random.randrange(20,60))

