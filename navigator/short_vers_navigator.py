import pandas as pd
import numpy as np
import random




import pandas as pd

url='https://drive.google.com/uc?id=1-crPzL6qMinByPzsrEHhGn1EJ1MfD3GX'
df = pd.read_csv(url, names=list(range(0, 100, 1)))
city_map_list = df.values.tolist()

city_map_list = np.array(city_map_list)





# Строим матрицы для каждого заказа, с запасом для удобства
orders_value_map = []
for i in range(len(orders_location)):
    temp_map = np.zeros((city_map_list.shape[0]+2, city_map_list.shape[1]+2))
    temp_map[1:-1,1:-1] = city_map_list[:,:]
    orders_value_map.append(temp_map)

# Выкалываем собственные координаты
    
for i in range(len(orders_value_map)):
    orders_value_map[i][orders_location[i][1]+1][orders_location[i][0]+1] = -1
    
courier_value_map = np.zeros((city_map_list.shape[0]+2, city_map_list.shape[1]+2))
courier_value_map[1:-1,1:-1] = city_map_list[:,:]
courier_value_map[courier_location[1]+1][courier_location[0]+1] = -1



# Функция вычисления стоимости, работает с условием того, что до любой проходимой точки можно добраться
import sys
sys.setrecursionlimit(10000)
def build_values_recursive(map, index):
    i = index[1]+1
    j = index[0]+1
    
    
    if map[i,j] == 1:
        adjacent_estimated = list(filter(lambda x: x != 0 and x != 1,[map[i,j+1], map[i,j-1], map[i+1,j], map[i-1,j]]))
        map[i,j] = int(min(adjacent_estimated) +10)
    if map[i,j] != 1:
        adjacent_not_estimated =list(filter(lambda x: map[x[0],x[1]] == 1,[(i,j+1), (i,j-1), (i+1,j), (i-1,j)]))
        for k in adjacent_not_estimated:
                ind = (k[1]-1, k[0]-1)
                build_values_recursive(map,ind)
                    
for i in range(len(orders_value_map)):
    build_values_recursive(orders_value_map[i], orders_location[i])

build_values_recursive(courier_value_map,courier_location)


# Поиск оптимального порядка доставок
def find_optimal_order(courier_value_map,orders_location,orders_value_map):
    courier_order_cost = []
    for i in orders_location:
        courier_order_cost.append(courier_value_map[i[1]+1,i[0]+1])
    orders_to_orders_cost = np.array([np.zeros(len(orders_location)) for _ in range(len(orders_location))])
    for i in range(len(orders_location)-1):
        for j in range(i+1,len(orders_location)):
            orders_to_orders_cost[i,j] = orders_value_map[i][orders_location[j][1]+1,orders_location[j][0]+1]
            orders_to_orders_cost[j,i] = orders_to_orders_cost[i,j]
            
    min_full_cost = max(courier_order_cost) + np.sum(orders_to_orders_cost)
    cheapest_path = []
    
    count_iterations = 0
    def calculate_minimum_cost_recursive(orders_to_orders_cost,path,summary):
        nonlocal count_iterations
        count_iterations+=1
        nonlocal min_full_cost
        nonlocal cheapest_path
        if len(path) == len(orders_location):
            if summary < min_full_cost:
                min_full_cost = summary
                cheapest_path = path
            return
        for i in range(len(orders_to_orders_cost)):
            if i in path:
                continue
            calculate_minimum_cost_recursive(orders_to_orders_cost, path+[i],summary+orders_to_orders_cost[path[-1],i])
    
    for i in range(len(courier_order_cost)):
        calculate_minimum_cost_recursive(orders_to_orders_cost, [i], courier_order_cost[i])
    print(count_iterations)
                
        
        
        
    return cheapest_path


def build_root(optimal_order, courier_location, courier_value_map, orders_location):
    route = []
    
    for i in range(-1,len(optimal_order)-1):
        temp = []
        curr = orders_location[optimal_order[i+1]]
        while(curr != courier_location):
            adjacent = list(filter( lambda x : courier_value_map[x[1]+1,x[0]+1] != 0, [(curr[0],curr[1]+1), (curr[0]+1,curr[1]), (curr[0],curr[1]-1), (curr[0]-1,curr[1])]))
            curr = min(adjacent, key = (lambda x: courier_value_map[x[1]+1,x[0]+1]))
            temp.append(curr)
        route.extend(temp[::-1])
        route.append(orders_location[optimal_order[i+1]])
        route.extend(temp)
    return route


optimal_order = find_optimal_order(courier_value_map,orders_location,orders_value_map)            
            
route = build_root(optimal_order, courier_location,courier_value_map,orders_location)