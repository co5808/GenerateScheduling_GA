import random
import ReadData
import matplotlib.pyplot as plt

#DNA 갯수s
GENE_POS = 4
GENS = 100
MUTATION = 0.001
CROSSOVER = 0.7
#분기별 예상 전기 소모량
EstimatePower = [80, 90, 65, 70]
GenerationDel = 0

#적합도 함수에 만족하지 못하는 하위 유전자 삭제 비율
#퍼센트(%) 단위로 기입하며, 0 이외의 수만 기입
ToRemove = 20
#종료 기준 Count -> 반복횟수, Fitness -> 목표 적합도 미만
Quit = ("Count", "Fitness")
#종료 기준 선택
QuitCond = Quit[0]

#반복 횟수 인수
MAX_GENERATION = 100

#목표 적합도
Target_Fitness = 1.0

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
            if Schedule[case+1][1] != 1:
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

    def mutation(self, CASE):
        #같은 염색체가 나타나는 것을 방지 하기 위한 반복문
        #print("Start mutation :", self.Gene, end='->')
        while(True):
            # random한 DNA 선택
            mutationDNA = random.randrange(0, CASE)
            #DNA 기본형태 선언
            #self.Gene[mutationDNA] = "0" * GENE_POS

            temp = list("0"*GENE_POS)

            mutation = random.randrange(0, len(temp))
            temp[mutation] = '1'
            #Scehdule은 1부터 7까지 존재.
            if GA.Schedule[mutationDNA+1][1] != 1:
                if mutation == len(temp) -1:
                    temp[0] = '1'
                else:
                    temp[mutation+1] = '1'
            #반면 Gene은 0부터 시작.
            if self.Gene[mutationDNA] != "".join(temp):
                self.Gene[mutationDNA] = "".join(temp)
                self.ProductPow()
                break
        print(self.Gene)
    #1점 교차(CrossOver) 방식
    def crossover(self, OtherGene):
        #print(self.Gene, "&" ,OtherGene.Gene, end="->")
        point = random.randrange(0, len(self.Gene))
        temp = self.Gene[point:]
        self.Gene[point:] = OtherGene.Gene[point:]
        OtherGene.Gene[point:] = temp
        mutationChois = random.randrange(1000)
        #print(self.Gene)
        if mutationChois == MUTATION * 1000:
            self.mutation(7)        #7은 유전자의 구분 종류

        self.ProductPow()
        return self

    def ProductPow(self):
        #분기별 총합량 계산
        self.GenerationCapa = []
        for i in range(0,4):
            temp = 0
            for j in range(1, len(self.Gene)+1):
                temp += GA.Schedule[j][0] * int(self.Gene[j-1][i])
                #print(GA.Schedule[j][0], int(self.Gene[j-1][i]))
            self.GenerationCapa.append(temp)
        #print(self.Gene,"\n", GA.Schedule,"\n", self.GenerationCapa)

def CalcFitness(Chromos, T):
    fitness = []
    total = 0
    for i in range(0, GENS):
        temp = 0
        #print(i, " )", end = "\t")
        #함수의 구성은 최종 생성 값이 0에 가까운 것.
        for j in range(0, GENE_POS):
            #150은 모든 장치가 가동 할 경우, 생성되는 최대 전력량
            # EstimatePower -> 각 분기당 필요 전력양
            # Chomos.GenerationCapa -> 각 분기당 수리로 인해 생산 할수 없는 전기의 양.

            # Fitness Function => 필요전기량 / 생산 전기량(전기 생산 가능 총량 - 분기별 생산 불가는 전력량)
            GenerationOutput = T - chromos[i].GenerationCapa[j]
            #if GenerationOutput != 0:
            if GenerationOutput != 0:
                temp += (EstimatePower[j] / GenerationOutput)
            else:
                print(i,chromos[i].GenerationCapa[j])
            #else:

            #total은 룰렛 선택을 적용하기 위한 전체 범주.
        total += temp
        #print("result = %d" %total)
        #tuple로 구성
        fitness.append( (temp, i) )
    fitness.sort(reverse=True)
    #print(total)
    return total, fitness

if __name__ == "__main__" :
    #chromos = Gene List

    chromos = []
    List, Count, TOTAL = ReadData.LoadSchedule()
    #랜덤한 유전자 생성
    while(True):
        temp = GA(List, Count)
        for j in range(0, len(EstimatePower)):
            #조건을 만족하지 못할 경우, 유전자 재생성
            if (TOTAL - temp.GenerationCapa[j]) < EstimatePower[j]:
                temp=None
                break
        if temp == None:
            continue
        else:
            #print(i, temp.Gene)
            chromos.append( temp )
            if len(chromos) == GENS:
                break


    #반복문을 이용한 세대 증가.
    Plots = []
    if QuitCond == "Count":
        Gen_COUNT = 0

    #세대 증가
    while(True):
        #각 세대당 삭제된 유전자 출력을 위한 변수
        GenerationDel = 0
        newChromos = []
        #FitTotal = 룰렛 선택 방법을 이용하기 위한 전체 돌림판의 크기
        #fitnesses =  (적합도, 인덱스) 튜플형태의 데이터가 들어있는 객체 리스트.

        FitTotal, fitnesses = CalcFitness(chromos, TOTAL)
        Plots.append(max(fitnesses)[0])
        #일정 비율의 부모를 제거 하기 위한 것이였으나 제거
        """
        if ToRemove != 0 and len(chromos) > (100 * ToRemove):
            newChromos.extend(chromos[:int(len(chromos) * (100 / ToRemove))])
            #print("leave Chromos", len(newChromos))
        """
        while(True):
            #첫번째 부모 선택
            # 0~100 사이의 수를 임의 선택
            SelectParent1 = random.randrange(100)           #0부터 round(FitTotal, 0) 사이의 랜덤한 수 (round(FitTotal, 0)은 0의 자리에서 버림한 수 )
            ranges = 0
            for i in range(0,len(chromos)):
                # 최적화 함수 역시 변경할 필요가 있음.
                #ranges += 1 - ( fitnesses[ i - 1 ] / FitTotal )
                #fitnesses = > ( 적합도, chromos No)
                ranges += (fitnesses[i][0] / FitTotal) * 100
                if ranges > SelectParent1:
                    Parent1 = chromos[fitnesses[i][1]]
                    break
                else:
                    if i == len(chromos):
                        print("What is wrong with you")
            #0~100 사이의 수를 임의 선택
            SelectParent2 = random.randrange(100)
            ranges = 0
            for i in range(0, len(chromos)):
                ranges += (fitnesses[i][0] / FitTotal) * 100
                if ranges > SelectParent2:
                    Parent2 = chromos[fitnesses[i][1]]
                    break
                else:
                    if i == len(chromos):
                        print("What is wrong with you")

            #교배(crossover)
            temp = Parent1.crossover(Parent2)
            for j in range(0, len(EstimatePower)):
                if (TOTAL - temp.GenerationCapa[j]) < EstimatePower[j] :
                    temp = None
                    break
            if temp == None:
                continue
            else:
                newChromos.append(temp)
                #한 세대의 유전자의 갯수를 유지하기 위한 조건문
                if len(newChromos) == GENS:
                    #for i in range(0,len(newChromos)):
                        #print(chromos[i].Gene, "->", newChromos[i].Gene)
                    chromos = newChromos.copy()
                    break


        # ------ 종료 기준 충족 확인 -----
        # 종료 기준이 "Count"일 경우
        if QuitCond == "Count":
            if Gen_COUNT == MAX_GENERATION:
                print(chromos[min(fitnesses)[1]])
                break
            else:
                Gen_COUNT += 1
                print("%d's Generation(fitTotal:%d)" %(Gen_COUNT,FitTotal))
        elif QuitCond == "Fitness":
            if fitnesses[0] < Target_Fitness:
                break

    plt.plot(Plots)
    plt.show()


