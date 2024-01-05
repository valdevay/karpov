import pandas as pd
from collections import deque
import numpy as np

city_map_list = [
    [1, 1, 0, 0, 1],
    [1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1],
]

courier_location = (1, 1)
orders_location = [(4, 4), (0, 4)]

map_file ="karpov-navigator\navigator_BSF\city_map.csv"

df = pd.read_csv(map_file, names=list(range(0, 100, 1)))
city_map_list = df.values.tolist()

city_map_list = np.array(city_map_list)


def is_valid_move(x, y, city_map):
    # Проверяем, находится ли координата в пределах города
    if x >= 0 and x < len(city_map[0]) and y >= 0 and y < len(city_map):
        # Проверяем, является ли район землей
        if city_map[y][x] == 1:
            return True
    return False

def get_available_moves(x, y, city_map):
    moves = []
    
    # Проверяем возможность перемещения влево
    if is_valid_move(x-1, y, city_map):
        moves.append((x-1, y))
    
    # Проверяем возможность перемещения вправо
    if is_valid_move(x+1, y, city_map):
        moves.append((x+1, y))
    
    # Проверяем возможность перемещения вверх
    if is_valid_move(x, y-1, city_map):
        moves.append((x, y-1))
    
    # Проверяем возможность перемещения вниз
    if is_valid_move(x, y+1, city_map):
        moves.append((x, y+1))
    
    return moves


def find_route(start, destinations, city_map):
    queue = deque()
    route = []
    visited = set()
    
    # Добавляем начальную позицию курьера в очередь
    queue.append(start)
    
    while queue:
        # Извлекаем текущую позицию из очереди
        current_position = queue.popleft()
        
        # Проверяем, является ли текущая позиция точкой назначения
        if current_position in destinations:
            route.append(current_position)
            destinations.remove(current_position)
            
            # Если все точки назначения доставлены, завершаем поиск
            if len(destinations) == 0:
                break
        
        # Получаем доступные позиции для перемещения
        available_moves = get_available_moves(current_position[0], current_position[1], city_map)
        
        for move in available_moves:
            # Проверяем, была ли уже посещена данная позиция
            if move not in visited:
                # Добавляем позицию в очередь и отмечаем ее как посещенную
                queue.append(move)
                visited.add(move)
                route.append(move)

    return route



if __name__ == '__main__':
    print(find_route(courier_location,orders_location,city_map_list))