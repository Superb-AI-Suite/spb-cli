# import random


# def make_random_color():
#     r = lambda: random.randint(0,255)
#     color = '#%02X%02X%02X' % (r(),r(),r())
#     return color


# def hex_to_rgb(value):
#     value = value.lstrip('#')
#     lv = len(value)
#     return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


# def rgb_to_hex(rgb):
#     return '#%02x%02x%02x' % rgb