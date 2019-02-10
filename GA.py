import random
import ReadData
#import matplotlib.pyploy as plt

#DNA 갯수s
GENE_POS = 4
GENS = 100
MUTATION = 0.001
CROSSOVER = 0.7
#분기별 예상 전기 소모량
EstimatePower = [80, 90, 65, 70]
MAX_GENERATION = 100

class GA(object):
    Schedule=[]
    def __init__(self, Schedule, CASE):
        self.Gene = []
        GA.Schedule = Schedule
        for case in range(0, CASE):
            self.Gene.append( '0' * GENE_POS)
            # 유전자 제약조건
            #1. 장치의 정비 기간은 처음에 시작하고 그 기간이나 인접한 바로 다음 기간에 끝난다.
            #(장비를 중단 할 수 없으며, 계획보다 일찍 끝냈수도 없다.)

            """
                    [ '0', '1', '0', '1' ]
                     
                       0,   1,   2,   3
            """
            # 0부터 3까지의 랜덤변수
            choice = random.randrange(4)
            #해당 위치의 정비스케줄 삽입
            temp = list(self.Gene[case])
            temp[choice] = '1'
            self.Gene[case] = "".join(temp)

            #print(Schedule[case + 1][1] != 1)
            if Schedule[case + 1][1] != 1:
                for index in range(1, Schedule[case + 1][1]):
                    #print(Schedule[case + 1][1] - 1)
                    temp = list(self.Gene[case])
                    if choice + index > (GENE_POS - 1):
                        #print(choice + index > (GENE_POS - 1))
                        temp[choice + index - (GENE_POS)] = '1'
                        #print(self.Gene[case], "=>", temp)
                    else:
                        temp[choice+index] = '1'
                        #print(self.Gene[case], "=>", temp)
                    self.Gene[case] = "".join(temp)
            self.ProductPow()

    def mutation(self, CASE):   # <- 제대로 작성된게 맞는 건가?
        #같은 염색체가 나타나는 것을 방지 하기 위한 반복문
        while(True):
            # random한 DNA 선택
            mutationDNA = random.randrange(1, CASE + 1)
            #DNA 기본형태 선언
            #self.Gene[mutationDNA] = "0" * GENE_POS

            temp = list("0"*GENE_POS)

            mutation = random.randrange(0, len(temp))
            temp[mutation] = '1'

            if GA.Schedule[mutationDNA][1] != 1:
                if mutation == len(temp) -1:
                    temp[0] = '1'
                else:
                    temp[mutation+1] = '1'
            if self.Gene[mutationDNA] != "".join(temp):
                self.Gene[mutationDNA] = "".join(temp)
                self.ProductPow()
                break

    def crossover(self, OtherGene):
        point = random.randrange(1, len(self.Gene))
        temp = self.Gene[point:]
        self.Gene[point:] = OtherGene.Gene[point:]
        OtherGene.Gene[point:] = temp
        mutationChois = random.randrange(1000)
        if mutationChois == MUTATION * 1000:
            self.mutation(7)        #7은 유전자의 구분 종류

        self.ProductPow()
        return self

    def ProductPow(self):
        #분기별 총합량 계산
        self.GenerationCapa = []

        for i in range(0,4):
            temp = 0
            for j in range(1, len(self.Gene)):
                temp += GA.Schedule[j][0] * int(self.Gene[j][i])
            self.GenerationCapa.append(temp)

def CalcFitness(Chromos, T):
    fitness = []
    total = 0
    for i in range(0, GENS):
        temp = 0
        print(i, " )", end = "\t")
        #함수의 구성은 최종 생성 값이 0에 가까운 것.
        for j in range(0, GENE_POS):
            #150은 모든 장치가 가동 할 경우, 생성되는 최대 전력량
            # EstimatePower -> 각 분기당 필요 전력양
            # Chromos.GenerationCapa -> 각 분기당 수리로 인해 생산 할수 없는 전기의 양.
            """
            temp += ( T - Chromos[i].GenerationCapa[j] ) - EstimatePower[j]
            print(" (%d - %d )  - %d = %d "%(T, Chromos[i].GenerationCapa[j], EstimatePower[j], temp), end="->")
            """
        print("result = %d" %temp)
        fitness.append(temp)
        total += temp
        print("TOTAL is ", total)
    return total, fitness

if __name__ == "__main__" :
    #chromos = Gene List

    chromos = []
    List, Count, TOTAL = ReadData.LoadSchedule()
    for i in range(0, GENS):
        temp = GA(List, Count)
        print(i, temp.Gene)
        chromos.append( temp )

    #반복문을 이용한 세대 증가.
    Generation = 0
    Plots = []
    while(True):
        newChromos = []
        #적합도 계산 -> 룰렛 휠 계산

        FitTotal, fitnesses = CalcFitness(chromos, TOTAL)

        Plots.append(min(fitnesses))
        print(Plots)
        # 새로운 세대 생성
        while(True):
            #첫번째 부모 선택
            SelectParent1 = random.randrange(100)           #0부터 100 사이의 랜덤한 수
            ranges = 0
            for i in range(1,len(chromos)+1):
                ranges += 1 - ( fitnesses[ i - 1 ] / FitTotal )
                if ranges > SelectParent1:
                    Parent1 = chromos[i - 1]


            SelectParent2 = random.randrange(100)
            ranges = 0
            for i in range(1, len(chromos)+1):
                ranges += 1 - ( fitnesses[i-1] / FitTotal )
                if ranges > SelectParent1:
                    Parent2 = chromos[i - 1]

            #교배(crossover)
            newChromos.append(Parent1.crossover(Parent2))

            #한 세대의 유전자의 갯수를 유지하기 위한 조건문
            if len(newChromos) == GENS:
                chromos = newChromos.copy()
                break
        print("Made Generation %d" % Generation)
        if Generation == MAX_GENERATION:
            break

        Generation += 1
"""
문제점 
1. 최저기준(각 분기 별 필요한 전기 생산량을 만드는지) -> 유전자 생성 시, 판단하여 제거할 것인지.
                                                 -> 다음 세대로 전이 될 때 제거할 것인지.
2. mutation과 crossover가 제대로 작동을 하는 것인지 확인할 필요 있음.
"""