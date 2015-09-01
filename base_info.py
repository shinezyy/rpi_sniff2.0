from update_time import get_current_time


pos_x = 3
pos_y = 4
position = dict()
position['x'] = pos_x
position['y'] = pos_y

my_id = 12345

def base_info():
    d = dict()
    d['update_time'] = get_current_time()
    d['pi_id'] = my_id
    d['position'] = position
    return d

