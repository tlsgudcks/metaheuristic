# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 23:54:32 2022

@author: parkh
"""
# ------ PSO Programming -----
# 목적함수의 최소해 구하기
# 탐색 중에 1번째,10번째,100번째,1000번째,10000번째 해집단의 분포를 보여주고 당시의 최소해를 표기
# ---------------------------

# ----- 해 구성 ------
# [x 좌표, y 좌표, 목적함수]로 구성된 list 타입의 해 사용: [0 ,0 ,0.0]
# x,y는 정해진 바운더리 내에서 벗어나지 않는다.
# --------------------

import random
import math
import copy
import matplotlib.pyplot as plt

params = {
    'POP_SIZE' : 50,  # population size 10 ~ 100
    'BOUNDARY' : 4, # 한 세대에 발생하는 자식 chromosome의 수
    'INERTIA_WEIGHT' : 0.5, # 관성 가중치
    'COGNITIVE_WEIGHT' : 1.0, # 인지 가중치 P_best
    'SOCIAL_WEIGHT': 1.0, # 사회 가중치 S_best
    'REPEAT': 200
    # 원하는 파라미터는 여기에 삽입할 것
    }

class PSO():
    def __init__(self, parameters):
        self.params = {}
        for key, value in parameters.items():
            self.params[key] = value
    
    def move(self, population, population_vector):
        #해들의 위치를 움직이는 함수
        for i in range(self.params["POP_SIZE"]):
            population[i][0] = population[i][0] + population_vector[i][0]
            population[i][1] = population[i][1] + population_vector[i][1]
        return population
    
    def population_condition(self, population): #함수 이름 변경
        #현재 위치하는 해들의 목적함수값을 갱신하는 함수
        for i in range(self.params["POP_SIZE"]):
            x=population[i][0]
            y=population[i][1]
            population[i][2] = -20*math.exp(-0.2*(0.5*(x**2+y**2))**1/2) - math.exp(0.5*(math.cos(2*math.pi*x) + math.cos(2*math.pi*y))) + math.e + 20
        return population
    
    def min_pop_con(self, population, min_pop):
        #해들이 지났던 위치 중 가장 낮은 값
        for i in range(self.params["POP_SIZE"]):
            if population[i][2] <= min_pop[i][2]:
                min_pop[i][0] = population[i][0]
                min_pop[i][1] = population[i][1]
                min_pop[i][2] = population[i][2]
        return min_pop
    
    def update_vector(self, population, population_vector, min_pop, min_condition):
        #벡터 방향을 업데이트 하는 함수
        for i in range(self.params["POP_SIZE"]):
            population_vector[i][0] = self.params["INERTIA_WEIGHT"]*population_vector[i][0]
            +self.params["COGNITIVE_WEIGHT"]*(min_pop[i][0]-population[i][0])
            +self.params["SOCIAL_WEIGHT"]*(min_condition[0]-population[i][0])
            population_vector[i][1] = self.params["INERTIA_WEIGHT"]*population_vector[i][1]
            +self.params["COGNITIVE_WEIGHT"]*(min_pop[i][1]-population[i][1])
            +self.params["SOCIAL_WEIGHT"]*(min_condition[1]-population[i][1])
        return population_vector
    
    def min_condition_population(self, min_pop, min_condition):
        #현재까지 가장 낮았던 해 위치와 목적함수를 반환
        for i in range(self.params["POP_SIZE"]):
            if min_pop[i][2] < min_condition[2]:
                min_condition = min_pop[i]
        return min_condition
    
    def search(self): 
        population = [] #초기해
        population_vector = [[0,0] for i in range(self.params["POP_SIZE"])] #초기 벡터 설정 [0,0]
        x = self.params["BOUNDARY"]
        y = self.params["BOUNDARY"]
        #가장 높은 목적함수를 갖고 있는 것으로 설정
        min_condition=[0,0,-20*math.exp(-0.2*(0.5*(x**2+y**2))**1/2)-math.exp(0.5*(math.cos(2*math.pi*x) + math.cos(2*math.pi*y))) + math.e + 20]
        
        #초기 해집단 생성
        for i in range(self.params["POP_SIZE"]):
            x=random.uniform(-self.params["BOUNDARY"], self.params["BOUNDARY"])
            y=random.uniform(-self.params["BOUNDARY"], self.params["BOUNDARY"])
            population.append([x,y,0])#목적함수가 들어갈 공간을 위해 0으로 설정
        population = self.population_condition(population) #리턴 x
        min_pop=copy.deepcopy(population)#깊은 복사로 초기 해집단 복사
        min_condition = self.min_condition_population(min_pop, min_condition)
        #반복 시행
        for i in range(self.params["REPEAT"]):
            if i%100 == 9 or i == 0:
                print(min_condition,i+1,"번째 최소해")
                print("-----------------------")
                x=[]
                y=[]
                for i in range(self.params["POP_SIZE"]):
                    x.append(population[i][0])
                    y.append(population[i][1])
                plt.scatter(x,y,alpha=0.5)
                plt.title("population")
                plt.axis([-self.params["BOUNDARY"],self.params["BOUNDARY"],-self.params["BOUNDARY"],self.params["BOUNDARY"]])
                plt.show()
                x=input("다음")
            # 벡터 계산
            population_vector = self.update_vector(population,population_vector,min_pop,min_condition)
            # 해집단 이동
            population = self.move(population,population_vector)
            # 해집단의 목적함수 변경
            population = self.population_condition(population)
            # 해집단 별로 가장 좋은 목적함수를 가진 위치를 저장
            min_pop = self.min_pop_con(population, min_pop)
            # 현재까지의 위치 중 목적함수가 가장 좋은 위치를 반환
            min_condition = self.min_condition_population(min_pop, min_condition)
            
if __name__ == "__main__":
    ga = PSO(params)
    ga.search()
