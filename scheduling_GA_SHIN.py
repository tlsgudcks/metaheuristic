# -*- coding: utf-8 -*-
"""
Created on Sun May 22 15:44:06 2022

@author: parkh
"""

import random
import copy
import pandas as pd
import numpy as np
# ----- 수정 가능한 파라미터 -----

params = {
    'MUT': 1,  # 변이확률(%)
    'END' : 0.9,  # 설정한 비율만큼 chromosome이 수렴하면 탐색을 멈추게 하는 파라미터 (%)
    'POP_SIZE' : 100,  # population size 10 ~ 100
    'RANGE' : 10, # chromosome의 표현 범위, 만약 10이라면 00000 00000 ~ 11111 11111까지임
    'NUM_OFFSPRING' : 5, # 한 세대에 발생하는 자식 chromosome의 수
    'SELECTION_PRESSURE' : 3, # 선택연산의 선택압
    'list_seq' : [1,2,3,4,5,6,7,8,9,10]
    # 원하는 파라미터는 여기에 삽입할 것
    }

#4,1,3,8,7,5,10,2,9,6
#3,1,4,2,9,6,7,8,10,5
# ------------------------------

dict_data = {"j1" :[3,7,1],"j2" :[5,17,2],"j3" :[2,9,3],
             "j4" :[4,6,2],"j5" :[11,18,1],"j6" :[7,14,3],
             "j7" :[8,12,1],"j8" :[9,12,2],"j9" :[6,13,2],
             "j10" :[10,21,1]}
df = pd.DataFrame(dict_data, index = ['p_time','d_date','weight'])
"""

data_num = 10

p_data = list(np.random.randint(2,8,size=data_num))
d_data = np.random.randint(10,20,size=data_num)
weight = np.random.randint(1,4,size=data_num)

ex = {}
for i in range(1,data_num+1):
    ex["j"+str(i)] = [p_data[i-1],d_data[i-1],weight[i-1]]
df = pd.DataFrame(ex, index = ['p_time','d_date','weight'])
"""
print(df)
#df=df2
#df.to_csv('C:/Users/parkh/scheduling2.csv')
#df.index = ['p_time','d_date','weight']

#df = pd.read_csv('C:/Users/parkh/scheduling2.csv')

class Ega_Scheduling():
    def __init__(self, parameters):
        self.params = {}
        for key, value in parameters.items():
            self.params[key] = value
            
    def enumaration_TotalFlowTime(self, df, chromosome):
        j=""
        columns=[]
        for i in chromosome:
            j = "j" + str(i)
            columns.append(j)
            j=""
        df_sorted = df[columns]
        lable1 = df_sorted.loc['p_time']
        total_flowTime = 0
        flowtime=0
        for i in lable1:
            flowtime = i + flowtime
            total_flowTime = total_flowTime + flowtime
        return total_flowTime
    
    def enumaration_TotalTardiness(self,df,chromosome):
        j=""
        columns=[]
        for i in chromosome:
            j = "j" + str(i)
            columns.append(j)
            j=""
        df_sorted = df[columns]
        lable1 = df_sorted.loc['p_time']
        lable2 = df_sorted.loc['d_date']
        flowtime=0
        flowtime_lst=[]
        tardiness_time=0
        due_date_lst=[]
        for i in lable1:
            flowtime = i + flowtime
            flowtime_lst.append(flowtime)
        for j in lable2:
            due_date_lst.append(j)
        for k in range(len(flowtime_lst)):
            tardiness_time = tardiness_time + (-1) * min(0, due_date_lst[k] - flowtime_lst[k])
        return tardiness_time

    def print_average_fitness(self, population):
        # todo: population의 평균 fitness를 출력
        population_average_fitness = 0
        total_population=0 
        for i in range(self.params["POP_SIZE"]):
            total_population=total_population+population[i][1]
        population_average_fitness=total_population/self.params["POP_SIZE"]
        print("population 평균 fitness: {}".format(population_average_fitness))

    def sort_population(self, population):
        population.sort(key=lambda x:x[1],reverse=False)
        # todo: fitness를 기준으로 population을 내림차순 정렬하고 반환
        
        return population

    def selection_operater(self, population):
        # todo: 본인이 원하는 선택연산 구현(룰렛휠, 토너먼트, 순위 등), 선택압을 고려할 것, 한 쌍의 부모 chromosome 반환
        mom_ch = []
        dad_ch = []
        fitness_population=copy.deepcopy(population) #리스트 복사
        total_score = 0 #유전자의 적합도 총합 계산
        sum_fitness = 0 #0부터 적합도들의 합을 더함 이것이 k보다 클 시 그 해를 선택
        #유전자별 적합도를 새로운 리스트에 입력
        for i in range(len(population)):
            fitness_population[i][1]=abs((population[-1][1]-population[i][1])-
            (population[0][1]-population[-1][1])/(self.params['SELECTION_PRESSURE']-1))
        #(Cw-Ci)+(Cb-Cw)/(k-1)
        
        #유전자의 적합도 총합계산
        for i in range(len(fitness_population)):
            total_score=fitness_population[i][1]+total_score
        total_score=int(total_score)
        #랜덤함수 호출        
        k=random.uniform(0, total_score)
        #룰렛 돌리기
        for i in range(len(fitness_population)):
            sum_fitness=sum_fitness+fitness_population[i][1]
            if sum_fitness>=k:
                dad_ch=fitness_population[i][0]
                fitness_population.pop(i)
                break
        #적합도 총합을 다시계산해줌, 더했던 적합도들의 합도 다시 계산
        sum_fitness=0
        total_score=0
        for i in range(len(fitness_population)):
            total_score=fitness_population[i][1]+total_score
        total_score=int(total_score)
        #랜덤함수 실행
        k2=random.uniform(0, total_score)
        #룰렛 돌리기
        for i in range(len(fitness_population)):
            sum_fitness=sum_fitness+fitness_population[i][1]
            if sum_fitness>=k2:
                mom_ch=fitness_population[i][0]
                break
        return mom_ch, dad_ch
        
    def crossover_operater(self, mom_cho, dad_cho):
        # todo: 본인이 원하는 교차연산 구현(point, pmx 등), 자식해 반환
        # 일점 교차를 사용함
        cut1=random.randint(0, self.params['RANGE']-5)
        cut2=cut1+3
        offspring_cho = [0 for x in range(self.params['RANGE'])]
        for i in range(cut1,cut2):
            offspring_cho[i] = mom_cho[i]
            dad_cho.remove(mom_cho[i])
        for i in range(cut2, self.params["RANGE"]):
            offspring_cho[i] = dad_cho[i-3]
        for i in range(0,cut1):
            offspring_cho[i] = dad_cho[i]
        return offspring_cho
    
    def crossover_operater2(self, mom_cho, dad_cho):
        # todo: 본인이 원하는 교차연산 구현(point, pmx 등), 자식해 반환
        # 일점 교차를 사용함
        cut=random.randint(1, self.params['POP_SIZE']-2)
        offspring_cho = [0,0,0,0,0,0,0,0,0,0]
        for i in range(3,6):
            offspring_cho[i] = mom_cho[i]
            dad_cho.remove(mom_cho[i])
        for i in range(6,10):
            offspring_cho[i] = dad_cho[i]
        for i in range(6,10):
            offspring_cho[i] = dad_cho[i-3]
        return offspring_cho

    def mutation_operater(self, chromosome):        
        # todo: 변이가 결정되었다면 chromosome 안에서 랜덤하게 지정된 하나의 gene를 반대의 값(0->1, 1->0)으로 변이
        point_cut1=random.randint(0, self.params['RANGE']-1)
        point_cut2=random.randint(0, self.params['RANGE']-1)
        chromosome[point_cut1],chromosome[point_cut2] = chromosome[point_cut2],chromosome[point_cut1]
        return chromosome

    def replacement_operator(self, population, offsprings):
        # todo: 생성된 자식해들(offsprings)을 이용하여 기존 해집단(population)의 해를 대치하여 새로운 해집단을 return
        """
        세대형 유전 알고리즘 사용
        해집단 내에서 가장 품질이 낮은 해를 대치하는 방법 사용(엘리티즘)
        """
        result_population = []
        for i in range(self.params["NUM_OFFSPRING"]):
            population.pop()
        for i in range(self.params["NUM_OFFSPRING"]):
            population.append([offsprings[i],
                               self.enumaration_TotalFlowTime(df, offsprings[i])])
        result_population=population[:]
        return result_population

    # 해 탐색(GA) 함수
    def search(self):
        generation = 0  # 현재 세대 수
        population = [] # 해집단
        offsprings = [] # 자식해집단
        
        # 1. 초기화: 랜덤하게 해를 초기화
        for i in range(self.params["POP_SIZE"]):
            random.shuffle(self.params["list_seq"])
            chromosome=[]
            for j in self.params["list_seq"]:
                chromosome.append(j)
            fitness=self.enumaration_TotalFlowTime(df, chromosome)
            population.append([chromosome,fitness])
        self.sort_population(population)
        print("initialzed population : \n", population, "\n\n")
        
        while 1:
            offsprings = []
            count_end=0 #동일 갯수
            for i in range(self.params["NUM_OFFSPRING"]):
                #offsprings = []                 
                # 2. 선택 연산
                mom_ch, dad_ch = self.selection_operater(population)

                # 3. 교차 연산
                offspring = self.crossover_operater(mom_ch, dad_ch)
                
                # 4. 변이 연산
                # todo: 변이 연산여부를 결정, self.params["MUT"]에 따라 변이가 결정되지 않으면 변이연산 수행하지 않음
                mute_development=random.uniform(0,100)
                if mute_development<self.params["MUT"]:
                    offspring = self.mutation_operater(offspring)
                offsprings.append(offspring)
            # 5. 대치 연산
            population = self.replacement_operator(population, offsprings)
            self.sort_population(population)
            self.print_average_fitness(population) # population의 평균 fitness를 출력함으로써 수렴하는 모습을 보기 위한 기능
            generation=generation+1
            # 6. 알고리즘 종료 조건 판단
            # todo population이 전체 중 self.params["END"]의 비율만큼 동일한 해를 갖는다면 수렴했다고 판단하고 탐색 종료
            for i in range(self.params["POP_SIZE"]):
                if population[0][1]==population[i][1]:
                    count_end=count_end+1
            if count_end/self.params["POP_SIZE"] >= self.params["END"]:
                print(population)
                print(count_end/self.params["POP_SIZE"])
                break

        # 최종적으로 얼마나 소요되었는지의 세대수, 수렴된 chromosome과 fitness를 출력
        print("탐색이 완료되었습니다. \t 최종 세대수: {},\t 최종 해: {},\t 최종 적합도: {}".format(generation, population[0][0], population[0][1]))
if __name__ == "__main__":
    ga = Ega_Scheduling(params)
    ga.search()
    print(df)