import string
import random
import os

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))


def check_id(id_x,path_id):
    t_id = path_id+id_x
    print(t_id)
    ex = os.path.exists(t_id)
    return ex


def Check_and_gen_ID(path_id):
    cond = True
    while(cond):
        id_i=id_generator()
        if check_id(id_i,path_id):
            cond = False
        else:
            break
    return id_i