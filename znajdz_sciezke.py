from astar_alghoritm import *


star_point = (8,2)
final_point = (14,11)
walls = [(12,9),(12,10),(12,11)]

route = Plan_Route(star_point, final_point, walls)
actions = astar_search(route).reconstruct_path()

print(actions)
