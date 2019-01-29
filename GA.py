import random
import ReadData

GENE_POS = 4
GENS = 100
MUTATION = 0.001
CROSSOVER = 0.7

class GA(object):
    def __init__(self, Schedule, CASE):
        self.Gene = []
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

    #돌연변이 관련 명령어
    def mutation(self, MutationRating):

    def crossover(self, OtherGene, CrossOverRate):

if __name__ == "__main__":
    #chromos = Gene List

    chromos = []
    List, Count, Total = ReadData.LoadSchedule()
    for i in range(0, GENS):
        chromos.append( GA(List, Count) )

