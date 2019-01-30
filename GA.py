import random
import ReadData

#DNA 갯수
GENE_POS = 4
GENS = 100
MUTATION = 0.001
CROSSOVER = 0.7

class GA(object):
    def __init__(self, Schedule, CASE):
        self.Gene = []
        self.Schedule = Schedule
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

    def mutation(self, Schedule, CASE):
        #같은 염색체가 나타나는 것을 방지 하기 위한 반복문
        while(True):
            # random한 DNA 선택
            mutationDNA = random.randrange(1, CASE + 1)
            #DNA 기본형태 선언
            #self.Gene[mutationDNA] = "0" * GENE_POS

            temp = list("0"*GENE_POS)

            mutation = random.randrange(0, len(temp))
            temp[mutation] = '1'

            if Schedule[mutationDNA][1] != 1:
                if mutation == len(temp) -1:
                    temp[0] = '1'
                else:
                    temp[mutation+1] = '1'
            if self.Gene[mutationDNA] != "".join(temp):
                self.Gene[mutationDNA] = "".join(temp)
                self.ProductPow()
                break

    def crossover(self, OtherGene):
        point = random.randomrange(1, len(self.Gene))
        temp = self.Gene[point:]
        self.Gene[point:] = OtherGene.Gene[point:]
        OtherGene.Gene[point:] = temp
        self.ProductPow()

    def ProductPow(self):
        #4분기 각각의 총합량 계산
        self.GenerationCapa = []
        for i in range(0,4):
            temp = 0
            for j in range(1, len(self.Gene)):
                temp += self.Schedule[j][0] * int(self.Gene[j][i])
            self.GenerationCapa.append(temp)

if __name__ == "__main__" :
    #chromos = Gene List

    chromos = []
    List, Count, Total = ReadData.LoadSchedule()
    for i in range(0, GENS):
        chromos.append( GA(List, Count) )

    #반복문을 이용한 세대 증가.