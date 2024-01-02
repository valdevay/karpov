import pandas as pd
import numpy as np
import random


import pandas as pd


courier_location = (10, 87)
orders_location = [(83, 38), (94, 56), (72, 75), (74, 64), (62, 15), (83, 99), (84, 25), (66, 7), (71, 41), (2, 40)]

url='https://drive.google.com/uc?id=1-crPzL6qMinByPzsrEHhGn1EJ1MfD3GX'
df = pd.read_csv(url, names=list(range(0, 100, 1)))
city_map_list = df.values.tolist()

city_map_list = np.array(city_map_list)

courier_value_map = np.zeros((city_map_list.shape[0]+2, city_map_list.shape[1]+2),dtype=tuple)
courier_value_map[1:-1,1:-1] = city_map_list[:,:]
courier_value_map[courier_location[1]+1][courier_location[0]+1] = (0,0,0,0)


# Функция вычисления стоимости, работает с условием того, что до любой проходимой точки можно добраться
import sys
sys.setrecursionlimit(100000)
def build_values_recursive(map, index):
    i = index[1]+1
    j = index[0]+1
    if map[i,j] == 1:
        adjacent_estimated = []
        if map[i,j+1] != 0 and map[i,j+1] != 1:
            adjacent_estimated.append((map[i,j+1][0]+1, map[i,j+1][1], map[i,j+1][2], map[i,j+1][3] ))
        if map[i,j-1] != 0 and map[i,j-1] != 1:
            adjacent_estimated.append((map[i,j-1][0], map[i,j-1][1]+1,map[i,j-1][2], map[i,j-1][3] ))
        if map[i+1,j] != 0 and map[i+1,j] != 1:
            adjacent_estimated.append((map[i+1,j][0], map[i+1,j][1],map[i+1,j][2]+1, map[i+1,j][3] ))
        if map[i-1,j] != 0 and map[i-1,j] != 1:
            adjacent_estimated.append((map[i-1,j][0], map[i-1,j][1],map[i-1,j][2], map[i-1,j][3]+1 ))
        map[i,j] = min(adjacent_estimated, key = lambda x: abs(x[0])+ abs(x[1])+abs(x[2])+ abs(x[3]))
        
        adjacent_estimated_coords = list(filter(lambda x: map[x] != 0 and map[x] != 1,[(i,j+1), (i,j-1), (i+1,j), (i-1,j)]))
        if map[i,j] != 1:
            for k,l in adjacent_estimated_coords:    
                if (map[k,l][0]-map[i,j][0]) + (map[k,l][1] - map[i,j][1]) +(map[k,l][2]-map[i,j][2]) + (map[k,l][3] - map[i,j][3]) > 1:
                        map[k,l] = 1
                        build_values_recursive(map,(l-1,k-1))
            
        
    if map[i,j] != 1:
        adjacent_not_estimated =list(filter(lambda x: map[x] == 1,[(i,j+1), (i,j-1), (i+1,j), (i-1,j)]))
        for k in adjacent_not_estimated:
                ind = (k[1]-1, k[0]-1)
                build_values_recursive(map,ind)
                


def find_optimal_order_simple(temp_courier,orders_location):
    route = []
    simple_path = [courier_location]
    n = len(orders_location)
    temp_courier = temp_courier.copy()
    while n:
        temp = 10000000
        mini = 0
        for i in range(len(orders_location)):
            if orders_location[i] not in simple_path:
                if temp > (temp_courier[orders_location[i][1]+1,orders_location[i][0]+1][0] + temp_courier[orders_location[i][1]+1,orders_location[i][0]+1][1]+ temp_courier[orders_location[i][1]+1,orders_location[i][0]+1][2] + temp_courier[orders_location[i][1]+1,orders_location[i][0]+1][3]):
                    temp = (temp_courier[orders_location[i][1]+1,orders_location[i][0]+1][0] + temp_courier[orders_location[i][1]+1,orders_location[i][0]+1][1]+ temp_courier[orders_location[i][1]+1,orders_location[i][0]+1][2] + temp_courier[orders_location[i][1]+1,orders_location[i][0]+1][3])
                    mini = i
        
        
        prev = simple_path[-1]
        simple_path.append(orders_location[mini])
        curr = simple_path[-1]
        temp = []
        failed = []
        while(curr != prev):
            adjacent = list(filter( lambda x : temp_courier[x[1]+1,x[0]+1] != 0, [(curr[0],curr[1]+1), (curr[0]+1,curr[1]), (curr[0],curr[1]-1), (curr[0]-1,curr[1])]))
            if (adjacent):
                curr = min(adjacent, key = (lambda x: abs(temp_courier[x[1]+1,x[0]+1][0])+ abs(temp_courier[x[1]+1,x[0]+1][1])+ abs(temp_courier[x[1]+1,x[0]+1][2]+ abs(temp_courier[x[1]+1,x[0]+1][3]))))
                temp.append(curr)
            else:
                failed.append(curr)
                curr = temp[-2]
                temp.pop()
                
        
                
            
            
        route.extend(temp[::-1])
        courier_value_map = np.zeros((city_map_list.shape[0]+2, city_map_list.shape[1]+2),dtype=tuple)
        courier_value_map[1:-1,1:-1] = city_map_list[:,:]
        courier_value_map[simple_path[-1][1]+1,simple_path[-1][0]+1] = (0,0,0,0)
        
        temp_courier = courier_value_map
        
        build_values_recursive(temp_courier,simple_path[-1])
        
        temp_courier[simple_path[-1][1]+1, simple_path[-1][0]+1] = (0,0,0,0)
                  
        
        n-=1
    route.append(simple_path[-1])
    return route
          
build_values_recursive(courier_value_map,courier_location)
route = find_optimal_order_simple(courier_value_map,orders_location)

print(len(route))