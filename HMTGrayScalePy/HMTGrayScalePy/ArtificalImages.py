from HMT import *
from Utils import *

#squares = zeros([800,800])
#squares[0:100,0:100] = 1
#squares[100:200,100:200] = 35
#squares[200:300,200:300] = 70
#squares[300:400,300:400] = 105
#squares[400:500,400:500] = 140
#squares[500:600,500:600] = 175
#squares[600:700,600:700] = 210
#squares[700:800,700:800] = 255
#saveImage(squares, 'squares', 'G:\\Felipe\\Mestrado\\ArtificialImages')

#KSHMT - com esse se ele acha os cantos dos quadrados e pico no cantinho inferior direito, é questão agora de fazer o thrshold certo e entender o porque o fundo vai mudando de cor ?
#squaresFG = uint8(array([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])) # - com esse se ele acha os cantos dos quadrados e pico no cantinho inferior direito, é questão agora de fazer o thrshold certo e entender o porque o fundo vai mudando de cor ?
#squaresFG = uint8(array([[1,0],[0,0]])) #- assim encontro as bordas superior e esquerda contudo, a altura dada ao array é igual ao resultado. tenho problemas aqui com o fundo preto

#squaresKS1 = ksHMT(squares, squaresFG)*-1
#squaresKS35 = ksHMT(squares, squaresFG*35)*-1
#squaresKS70 = ksHMT(squares, squaresFG*70)*-1
#squaresKS105 = ksHMT(squares, squaresFG*105)*-1
#squaresKS140 = ksHMT(squares, squaresFG*140)*-1
#squaresKS175 = ksHMT(squares, squaresFG*175)*-1
#squaresKS210 = ksHMT(squares, squaresFG*210)*-1
#squaresKS255 = ksHMT(squares, squaresFG*255)*-1

#saveImage(squaresKS1, 'squaresKS1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresKS35 , 'squaresKS35', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresKS70 , 'squaresKS70', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresKS105, 'squaresKS105', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresKS140, 'squaresKS140', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresKS175, 'squaresKS175', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresKS210, 'squaresKS210', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresKS255, 'squaresKS255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')

##SUHMT 
#squaresFG = uint8(array([[2,2,2],[2,2,2],[2,2,2]]))
#squaresBG = uint8(array([[1,1,1],[1,1,1],[1,1,1]]))
#squaresFG = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
#squaresBG = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))
#squaresSU1 = suHMT(squares, squaresFG, squaresBG)
#saveImage(squaresSU1, 'squaresSU1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#squaresSU1Dilated = iadil(uint8(squaresSU1), iasebox(50))
#saveImage(squaresSU1Dilated, 'squaresSU1Dilated', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')

##BHMT
#squaresFG = array([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]) # com esses SEs tenho um resultado esquisito: ele acha as bordas e elas tem valores que variam inversamnte com o valor do SE, o fundo tambem muda de cor... - esses SES tb trazem valores maiores que 255..pelo artigo esses são os piores matches já que lower values são melhores matches - se o se for iabinary da o mesmo problema. com relação ao fundo q muda de cor, é devido ao estouro de 255
#squaresBG = iasereflect(ianeg(array([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

#squaresB1 = bHMT(squares, squaresFG, squaresBG)
#squaresB35 = bHMT(squares, squaresFG*35, squaresBG*35)
#squaresB70 = bHMT(squares, squaresFG*70, squaresBG*70)
#squaresB105 = bHMT(squares, squaresFG*105, squaresBG*105)
#squaresB140 = bHMT(squares, squaresFG*140, squaresBG*140)
#squaresB175 = bHMT(squares, squaresFG*175, squaresBG*175)
#squaresB210 = bHMT(squares, squaresFG*210, squaresBG*210)
#squaresB255 = bHMT(squares, squaresFG*255, squaresBG*255)

#saveImage(squaresB1, 'squaresB1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresB35 , 'squaresB35', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresB70 , 'squaresB70', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresB105, 'squaresB105', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresB140, 'squaresB140', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresB175, 'squaresB175', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresB210, 'squaresB210', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresB255, 'squaresB255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')

##RHMT
#squaresFG = array([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]) # esses ses trazem os quadrados sem um pedaço de borda. os valores estouram 255 e por isso variam bastante.o fundo tambem muda a intensidade. me parece que é o melhor caso já que traz o quadrado inteiro e avaliano corretamente a altura do se, cnsigo retirar objetos com alura menor que uma desejada, contudo isso relfete nos valores obtidos na saida da operacao. Quando o quadrado avaliado é da mesma altura do se, o resultado vem com 0 na posição. então 0 aqui é o melhor match (?verificar)
#squaresBG = iasereflect(ianeg(array([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

#squaresR1 = rHMT(squares, squaresFG, squaresBG)
#squaresR35 = rHMT(squares, squaresFG*35, squaresBG*35)
#squaresR70 = rHMT(squares, squaresFG*70, squaresBG*70)
#squaresR105 = rHMT(squares, squaresFG*105, squaresBG*105)
#squaresR140 = rHMT(squares, squaresFG*140, squaresBG*140)
#squaresR175 = rHMT(squares, squaresFG*175, squaresBG*175)
#squaresR210 = rHMT(squares, squaresFG*210, squaresBG*210)
#squaresR255 = rHMT(squares, squaresFG*255, squaresBG*255)

#saveImage(squaresR1, 'squaresR1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresR35 , 'squaresR35', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresR70 , 'squaresR70', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresR105, 'squaresR105', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresR140, 'squaresR140', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresR175, 'squaresR175', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresR210, 'squaresR210', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresR255, 'squaresR255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')

#RGHMT
#squaresFG = array([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]) # com esses SEs, o fundo vai guanhando a cor do inverso da altura do SE e os quadrados com altura menores/igual a cor do SE vao sendo removidos
#squaresBG = iasereflect(ianeg(array([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

#squaresRG1 = rgHMT(squares, squaresFG, squaresBG)
#squaresRG35 = rgHMT(squares, squaresFG*35, squaresBG*35)
#squaresRG70 = rgHMT(squares, squaresFG*70, squaresBG*70)
#squaresRG105 = rgHMT(squares, squaresFG*105, squaresBG*105)
#squaresRG140 = rgHMT(squares, squaresFG*140, squaresBG*140)
#squaresRG175 = rgHMT(squares, squaresFG*175, squaresBG*175)
#squaresRG210 = rgHMT(squares, squaresFG*210, squaresBG*210)
#squaresRG255 = rgHMT(squares, squaresFG*255, squaresBG*255)

#saveImage(squaresRG1, 'squaresRG1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresRG35 , 'squaresRG35', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresRG70 , 'squaresRG70', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresRG105, 'squaresRG105', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresRG140, 'squaresRG140', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresRG175, 'squaresRG175', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresRG210, 'squaresRG210', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresRG255, 'squaresRG255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')


#POHMT - aqui tenho que testar com ruido e variando o valor de P - a implementação está horrivel e demorando demais....
#squaresFG = array([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
#squaresBG = iasereflect(ianeg(array([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

#squaresPO1 = poHMT(squares, squaresFG, squaresBG, 100)
#squaresPO35 = poHMT(squares, squaresFG*35, squaresBG*35, 100)
#squaresPO70 = poHMT(squares, squaresFG*70, squaresBG*70, 100)
#squaresPO105 = poHMT(squares, squaresFG*105, squaresBG*105, 100)
#squaresPO140 = poHMT(squares, squaresFG*140, squaresBG*140, 100)
#squaresPO175 = poHMT(squares, squaresFG*175, squaresBG*175, 100)
#squaresPO210 = poHMT(squares, squaresFG*210, squaresBG*210, 100)
#squaresPO255 = poHMT(squares, squaresFG*255, squaresBG*255, 100)

#saveImage(squaresPO1, 'squaresPO1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresPO35 , 'squaresPO35', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresPO70 , 'squaresPO70', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresPO105, 'squaresPO105', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresPO140, 'squaresPO140', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresPO175, 'squaresPO175', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresPO210, 'squaresPO210', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(squaresPO255, 'squaresPO255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')


#degrade = zeros([800,800])
#degrade[0:100,] = 0
#degrade[100:200,] = 35
#degrade[200:300,] = 70
#degrade[300:400,] = 105
#degrade[400:500,] = 140
#degrade[500:600,] = 175
#degrade[600:700,] = 210
#degrade[700:800,] = 255
#saveImage(degrade, 'degrade', 'G:\\Felipe\\Mestrado\\ArtificialImages')

#degradeFG = uint8(ones((1,800)))
#degradeKS1 = ksHMT(degrade, degradeFG)*-1
#degradeKS35 = ksHMT(degrade, degradeFG*35)*-1
#degradeKS70 = ksHMT(degrade, degradeFG*70)*-1
#degradeKS105 = ksHMT(degrade, degradeFG*105)*-1
#degradeKS140 = ksHMT(degrade, degradeFG*140)*-1
#degradeKS175 = ksHMT(degrade, degradeFG*175)*-1
#degradeKS210 = ksHMT(degrade, degradeFG*210)*-1
#degradeKS255 = ksHMT(degrade, degradeFG*255)*-1

#saveImage(degradeKS1, 'degradeKS1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(degradeKS35 , 'degradeKS35', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(degradeKS70 , 'degradeKS70', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(degradeKS105, 'degradeKS105', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(degradeKS140, 'degradeKS140', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(degradeKS175, 'degradeKS175', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(degradeKS210, 'degradeKS210', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')
#saveImage(degradeKS255, 'degradeKS255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\output')



#disks = zeros([800,800], dtype='uint8')
#disks[50,50] = 30
#disks[150,150] = 60
#disks[250,250] = 90
#disks[350,350] = 120
#disks[450,450] = 150
#disks[550,550,] = 180
#disks[650,650] = 210
#disks[750,750] = 250
#disks = iadil(disks, iasedisk(50))
#saveImage(disks, 'disks', 'G:\\Felipe\\Mestrado\\ArtificialImages')








#####################################################
### GERANDO EXEMPLOS PARA A SEÇÃO DE SES FLAT
#####################################################
#squares = zeros([800,800])
#squares[0:100,0:100] = 20
#squares[100:200,100:200] = 35
#squares[200:300,200:300] = 70
#squares[300:400,300:400] = 105
#squares[400:500,400:500] = 140
#squares[500:600,500:600] = 175
#squares[600:700,600:700] = 210
#squares[700:799,700:799] = 255
#saveImage(ianeg(uint8(squares)), 'squares', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat')

#degrade = zeros([800,800])
#degrade[0:100,] = 0
#degrade[100:200,] = 35
#degrade[200:300,] = 70
#degrade[300:400,] = 105
#degrade[400:500,] = 140
#degrade[500:600,] = 175
#degrade[600:700,] = 210
#degrade[700:800,] = 255
#saveImage(degrade, 'degrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat')

#disks = zeros([800,800], dtype='uint8')
#disks[50,50] = 30
#disks[150,150] = 60
#disks[250,250] = 90
#disks[350,350] = 120
#disks[450,450] = 150
#disks[550,550,] = 180
#disks[650,650] = 210
#disks[750,750] = 250
#disks = iadil(disks, iasedisk(50))
#saveImage(disks, 'disks', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat')

###########QUADRADOS
##KSHMT - com esse se ele acha os cantos dos quadrados e pico no cantinho inferior direito, é questão agora de fazer o thrshold certo e entender o porque o fundo vai mudando de cor ?
#squaresFG = uint8(array([[1,0,0],[0,0,0],[0,0,1]]))
#saveImage(iaseshow(bool_(squaresFG), 'expand')*255, 'squaresKS1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#squaresKS1 = ksHMT(squares, squaresFG)+255
#squaresKS1[squaresKS1 > 255] = 0 #fixing overflow
#saveImage(squaresKS1, 'squaresKS1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#squaresKS255 = ksHMT(squares, squaresFG*255)+255
#squaresKS255[squaresKS255 > 255] = 0 #fixing overflow
#saveImage(ianeg(uint8(squaresKS255)), 'squaresKS1_255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

###SUHMT 
##squaresFG = uint8(array([[1,0,0],[0,0,0],[0,0,1]]))
##squaresBG = uint8(array([[1,1,1],[1,1,1],[1,1,1]]))
#squaresFG = iabinary([[1,0,0],[0,0,0],[0,0,1]])
#squaresBG = iabinary([[1,1,0],[1,1,1],[0,1,1]])
#saveImage(iaseshow(bool_(squaresFG), 'expand')*255, 'squaresSU1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(iasereflect(ianeg(squaresBG))), 'expand')*255, 'squaresSU1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#squaresSU1 = suHMT(squares, squaresFG, squaresBG)
#saveImage(ianeg(uint8(squaresSU1)), 'squaresSU1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#squaresSU1Dilated = iadil(uint8(squaresSU1), iasebox(20))
#saveImage(ianeg(uint8(squaresSU1Dilated)), 'squaresSU1Dilated', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#squaresSU255 = suHMT(squares, uint8(squaresFG)*255, uint8(squaresBG*255))
#saveImage(ianeg(uint8(squaresSU255)), 'squaresSU255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#squaresSU255Dilated = iadil(uint8(squaresSU255), iasebox(20))
#saveImage(ianeg(uint8(squaresSU255Dilated)), 'squaresSU255Dilated', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')



##BHMT 
#squaresFG = uint8(array([[1,0,0],[0,0,0],[0,0,1]]))
#squaresBG = uint8(array([[0,0,1],[0,0,0],[1,0,0]]))
#saveImage(iaseshow(bool_(squaresFG), 'expand')*255, 'squaresB1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(squaresBG), 'expand')*255, 'squaresB1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#squaresB1 = bHMT(squares, squaresFG, squaresBG)
#saveImage(ianeg(uint8(squaresB1)), 'squaresB1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##squaresB255 = bHMT(squares, uint8(squaresFG)*255, uint8(squaresBG*255))
##saveImage(ianeg(uint8(squaresB255)), 'squaresB255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')


##RHMT 
#squaresFG = uint8(array([[1,0,0],[0,0,0],[0,0,1]]))
#squaresBG = uint8(array([[0,0,1],[0,0,0],[1,0,0]]))
#saveImage(iaseshow(bool_(squaresFG), 'expand')*255, 'squaresR1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(squaresBG), 'expand')*255, 'squaresR1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#squaresR1 = rHMT(squares, squaresFG, squaresBG)
#saveImage(ianeg(uint8(squaresR1)), 'squaresR1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##squaresB255 = bHMT(squares, uint8(squaresFG)*255, uint8(squaresBG*255))
##saveImage(ianeg(uint8(squaresB255)), 'squaresB255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')


##RGHMT 
#squaresFG = uint8(array([[1,0,0],[0,0,0],[0,0,1]]))
#squaresBG = uint8(array([[0,0,1],[0,0,0],[1,0,0]]))
#saveImage(iaseshow(bool_(squaresFG), 'expand')*255, 'squaresRG1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(squaresBG), 'expand')*255, 'squaresRG1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#squaresRG1 = rgHMT(squares, squaresFG, squaresBG)
#saveImage(ianeg(uint8(squaresRG1)), 'squaresRG1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
##############FIM QUADRADOS

##############DISCOS
#disks = openImage("G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\disks.png")
#saveImage(ianeg(disks), 'disks', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
##KSHMT
#disksFG = uint8(iasecross(3))
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksKS1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksKS1 = ksHMT(disks, disksFG)+255
#disksKS1[disksKS1 > 255] = 0 #fixing overflow
#saveImage(disksKS1, 'disksKS1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksKS255 = ksHMT(disks, disksFG*255)+255
#disksKS255[disksKS255 > 255] = 0 #fixing overflow
#saveImage(ianeg(uint8(disksKS255)), 'disksKS1_255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')


###SUHMT 
#disksFG = ianeg(iaero(iasedisk(3), iasedisk()))
#disksBG = iasedisk(50)
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksSU1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(disksBG*255, 'disksSU1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksSU1 = suHMT(disks, disksFG, disksBG)
#saveImage(ianeg(uint8(disksSU1)), 'disksSU1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#disksSU1Dilated = iadil(uint8(disksSU1), iasedisk(10))
#saveImage(ianeg(uint8(disksSU1Dilated)), 'disksSU1Dilated', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#BHMT 
#disksFG = iasedisk()
#disksBG = iasedisk(5)
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksB1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(disksBG), 'expand')*255, 'disksB1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksB1 = bHMT(disks, disksFG, disksBG)
#saveImage(ianeg(uint8(disksB1)), 'disksB1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#RGHMT 
#disksFG = iasedisk()
#disksBG = ianeg(iasedisk())
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksRG1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(disksBG), 'expand')*255, 'disksRG1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksRG1 = rgHMT(disks, disksFG, disksBG)
#saveImage(ianeg(uint8(disksRG1)), 'disksRG1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##############FIM DISCOS



##############DISCOS GRADIENT
#diskDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegrade.png')
#diskDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
##disks = zeros([800,800], dtype='uint8')
##disks[50,50] = 30
##disks[150,150] = 60
##disks[250,250] = 90
##disks[350,350] = 120
##disks[450,450] = 150
##disks[550,550,] = 180
##disks[650,650] = 210
##disks[750,750] = 250
##disks = iadil(disks, diskDegrade)
##saveImage(disks, 'disksDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\')
#disks = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\disks.png')
#disksDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\disksDegrade.png')
##saveImage(ianeg(disksDegrade), 'disksDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##KSHMT
#disksFG = uint8(iasecross(3))
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksDegradeKS1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-non-flat \ se-flat
#disksDegradeKSFG = ksHMT(disksDegrade, disksFG)+255
#disksDegradeKSFG[disksDegradeKSFG > 255] = 0 #fixing overflow
#saveImage(disksDegradeKSFG, 'disksDegradeKSFG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-non-flat \ se-non-flat
#disksDegradeKSFGDegrade = ksHMT(disksDegrade, diskDegrade)+255
#disksDegradeKSFGDegrade[disksDegradeKSFGDegrade > 255] = 0 #fixing overflow
#saveImage(ianeg(disksDegradeKSFGDegrade), 'disksDegradeKSFGDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-flat \ se-non-flat
#disksKSFGDegrade = ksHMT(disks, diskDegrade)+255
#disksKSFGDegrade[disksKSFGDegrade > 255] = 0 #fixing overflow
#saveImage(ianeg(disksKSFGDegrade), 'disksKSFGDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')




###SUHMT 
#flat ses
#disksFG = ianeg(iaero(iasedisk(3), iasedisk()))
#disksBG = iasedisk(50)
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksSU1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(disksBG*255, 'disksSU1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#non-flat ses
#disksNonFlatFG = diskDegrade
#disksNonFlatFG.flags.writeable=True
#disksNonFlatFG[15,15] = 0
#diskDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
#disksNonFlatBG = int16(diskDegrade) - 50
#disksNonFlatBG[disksNonFlatBG<0] = 0
#disksNonFlatBG = uint8(disksNonFlatBG)
#saveImage(disksNonFlatFG, 'disksSUNonFlatFG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(disksNonFlatBG, 'disksSUNonFlatBG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#IMG-non-flat \ se-flat
#disksDegradeSUFG = suHMT(disksDegrade, disksFG, disksBG)
#saveImage(ianeg(uint8(disksDegradeSUFG)), 'disksDegradeSUFG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#disksDegradeSUFGDilated = iadil(uint8(disksDegradeSUFG), iasedisk(10))
#saveImage(ianeg(uint8(disksDegradeSUFGDilated)), 'disksDegradeSUFGDilated', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#IMG-flat \ se-non-flat # SUHMT dont work with flat SEs
#disksSUDegradeFG = suHMT(disks, disksNonFlatFG, disksNonFlatBG)
#saveImage(ianeg(uint8(disksSUDegradeFG)), 'disksSUDegradeFG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#disksSUDegradeFGDilated = iadil(uint8(disksSUDegradeFG), iasedisk(10))
#saveImage(ianeg(uint8(disksSUDegradeFGDilated)), 'disksSUDegradeFGDilated', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-non-flat \ se-non-flat
#disksDegradeSUDegradeFG = suHMT(disksDegrade, disksNonFlatFG, disksNonFlatBG)
#saveImage(ianeg(uint8(disksDegradeSUDegradeFG)), 'disksDegradeSUDegradeFG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#disksDegradeSUDegradeFGDilated = iadil(uint8(disksDegradeSUDegradeFG), iasedisk(10))
#saveImage(ianeg(uint8(disksDegradeSUDegradeFGDilated)), 'disksDegradeSUDegradeFGDilated', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')


#BHMT 
#disksFG = iasedisk()
#disksBG = iasedisk(5)
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksB1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(disksBG), 'expand')*255, 'disksB1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksFGDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
#disksBGDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
#disksBGDegrade = int16(disksBGDegrade) - 50
#disksBGDegrade[disksBGDegrade<0] = 0
#disksBGDegrade = uint8(disksBGDegrade)

#saveImage(disksFGDegrade, 'disksFGDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(disksBGDegrade, 'disksBGDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-non-flat \ se-flat
#disksDegradeB = bHMT(disksDegrade, disksFG, disksBG)
#saveImage(ianeg(uint8(disksDegradeB)), 'disksDegradeB', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-flat \ se-non-flat 
#disksBDegrade = bHMT(disks, disksFGDegrade, disksBGDegrade)
#saveImage(ianeg(uint8(disksBDegrade)), 'disksBDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-non-flat \ se-non-flat
#disksDegradeBDegrade = bHMT(disksDegrade, disksFGDegrade, disksBGDegrade)
#saveImage(ianeg(uint8(disksDegradeBDegrade)), 'disksDegradeBDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')


#RGHMT 
#disksFG = iasedisk()
#disksBG = ianeg(iasedisk())
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksRG1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(disksBG), 'expand')*255, 'disksRG1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksFGDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
#disksBGDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
#disksBGDegrade = int16(disksBGDegrade) - 50
#disksBGDegrade[disksBGDegrade<0] = 0
#disksBGDegrade = uint8(disksBGDegrade)

##IMG-non-flat \ se-flat
#disksDegradeRG = rgHMT(disksDegrade, disksFG, disksBG)
#saveImage(ianeg(uint8(disksDegradeRG)), 'disksDegradeRG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-flat \ se-non-flat 
#disksRGDegrade = rgHMT(disks, disksFGDegrade, disksBGDegrade)
#saveImage(ianeg(uint8(disksRGDegrade)), 'disksRGDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output') #solta imagem preta

#saveImage(ianeg(uint8(openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output\\disksRGDegrade.png'))), 'disksRGDegradeNeg', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#IMG-non-flat \ se-non-flat
#disksDegradeRGDegrade = rgHMT(disksDegrade, disksFGDegrade, disksBGDegrade)
#saveImage(ianeg(uint8(disksDegradeRGDegrade)), 'disksDegradeRGDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(ianeg(uint8(openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output\\disksDegradeRGDegrade.png'))), 'disksDegradeRGDegradeNeg', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
##############FIM DISCOS GRADIENT



##???????????????????????????????????????????????????????????????



##############RUIDOS DISCOS GRADIENT
#diskDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegrade.png')
diskDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
##disks = zeros([800,800], dtype='uint8')
##disks[50,50] = 30
##disks[150,150] = 60
##disks[250,250] = 90
##disks[350,350] = 120
##disks[450,450] = 150
##disks[550,550,] = 180
##disks[650,650] = 210
##disks[750,750] = 250
##disks = iadil(disks, diskDegrade)
##saveImage(disks, 'disksDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\')
disks = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\disks.png')
disksDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\disksDegrade.png')
##saveImage(ianeg(disksDegrade), 'disksDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#adding noise
#disksNoise = disks + util.random_noise(disks, 's&p', 99, amount=0.02)*random.rand(disks.shape[0], disks.shape[1])*255
#saveImage(disksNoise, 'disksNoise', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#disksDegradeNoise = disksDegrade + util.random_noise(disksDegrade, 's&p', 99, amount=0.02)*random.rand(disksDegrade.shape[0], disksDegrade.shape[1])*255
#saveImage(disksDegradeNoise, 'disksDegradeNoise', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

disksNoise = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\disksNoise.png')
disksDegradeNoise = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\disksDegradeNoise.png')


#removing noise from flat disks
###KSHMT
#disksFG = uint8(iasecross(3))
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksKS1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksNoiseKS1 = ksHMT(disksNoise, disksFG)+255
#disksNoiseKS1[disksNoiseKS1 > 255] = 0 #fixing overflow
#saveImage(disksNoiseKS1, 'disksNoiseKS1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksNoiseKS255 = ksHMT(disksNoise, disksFG*255)+255
#disksNoiseKS255[disksNoiseKS255 > 255] = 0 #fixing overflow
#saveImage(ianeg(uint8(disksNoiseKS255)), 'disksNoiseKS1_255', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

###SUHMT 
#disksFG = ianeg(iaero(iasedisk(3), iasedisk()))
#disksBG = iasedisk(50)
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksSU1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(disksBG*255, 'disksSU1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksNoiseSU1 = suHMT(disksNoise, disksFG, disksBG)
#saveImage(ianeg(uint8(disksNoiseSU1)), 'disksNoiseSU1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#disksNoiseSU1Dilated = iadil(uint8(disksNoiseSU1), iasedisk(10))
#saveImage(ianeg(uint8(disksNoiseSU1Dilated)), 'disksNoiseSU1Dilated', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#BHMT 
#disksFG = iasedisk()
#disksBG = iasedisk(5)
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksB1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(disksBG), 'expand')*255, 'disksB1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksNoiseB1 = bHMT(disksNoise, disksFG, disksBG)
#saveImage(ianeg(uint8(disksNoiseB1)), 'disksNoiseB1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#RGHMT 
#disksFG = iasedisk()
#disksBG = ianeg(iasedisk())
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksRG1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(disksBG), 'expand')*255, 'disksRG1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksNoiseRG1 = rgHMT(disksNoise, disksFG, disksBG)
#saveImage(ianeg(uint8(disksNoiseRG1)), 'disksNoiseRG1', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')



#end flat disks noise



#removing noise from non-flat  disks
##KSHMT
#disksFG = uint8(iasecross(3))
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksDegradeNoiseKS1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

###se-flat
#disksDegradeNoiseKSFG = ksHMT(disksDegradeNoise, disksFG)+255
#disksDegradeNoiseKSFG[disksDegradeNoiseKSFG > 255] = 0 #fixing overflow
#saveImage(disksDegradeNoiseKSFG, 'disksDegradeNoiseKSFG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

####se-non-flat
#disksDegradeNoiseKSFGDegrade = ksHMT(disksDegradeNoise, diskDegrade)+255
#disksDegradeNoiseKSFGDegrade[disksDegradeNoiseKSFGDegrade > 255] = 0 #fixing overflow
#saveImage(ianeg(disksDegradeNoiseKSFGDegrade), 'disksDegradeNoiseKSFGDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')


###SUHMT 
##flat ses
#disksFG = ianeg(iaero(iasedisk(3), iasedisk()))
#disksBG = iasedisk(50)
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksSU1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(disksBG*255, 'disksSU1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##non-flat ses
#disksNonFlatFG = diskDegrade
#disksNonFlatFG.flags.writeable=True
#disksNonFlatFG[15,15] = 0
#diskDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
#disksNonFlatBG = int16(diskDegrade) - 50
#disksNonFlatBG[disksNonFlatBG<0] = 0
#disksNonFlatBG = uint8(disksNonFlatBG)
#saveImage(disksNonFlatFG, 'disksSUNonFlatFG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(disksNonFlatBG, 'disksSUNonFlatBG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-non-flat \ se-flat
#disksDegradeNoiseSUFG = suHMT(disksDegradeNoise, disksFG, disksBG)
#saveImage(ianeg(uint8(disksDegradeNoiseSUFG)), 'disksDegradeNoiseSUFG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#disksDegradeNoiseSUFGDilated = iadil(uint8(disksDegradeNoiseSUFG), iasedisk(10))
#saveImage(ianeg(uint8(disksDegradeNoiseSUFGDilated)), 'disksDegradeNoiseSUFGDilated', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#IMG-flat \ se-non-flat # SUHMT dont work with non-flat SEs
#disksSUDegradeFG = suHMT(disks, disksNonFlatFG, disksNonFlatBG)
#saveImage(ianeg(uint8(disksSUDegradeFG)), 'disksSUDegradeFG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#disksSUDegradeFGDilated = iadil(uint8(disksSUDegradeFG), iasedisk(10))
#saveImage(ianeg(uint8(disksSUDegradeFGDilated)), 'disksSUDegradeFGDilated', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-non-flat \ se-non-flat
#disksDegradeSUDegradeFG = suHMT(disksDegrade, disksNonFlatFG, disksNonFlatBG)
#saveImage(ianeg(uint8(disksDegradeSUDegradeFG)), 'disksDegradeSUDegradeFG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#disksDegradeSUDegradeFGDilated = iadil(uint8(disksDegradeSUDegradeFG), iasedisk(10))
#saveImage(ianeg(uint8(disksDegradeSUDegradeFGDilated)), 'disksDegradeSUDegradeFGDilated', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')


#BHMT 
#disksFG = iasedisk()
#disksBG = iasedisk(5)
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksB1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(disksBG), 'expand')*255, 'disksB1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksFGDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
#disksBGDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
#disksBGDegrade = int16(disksBGDegrade) - 50
#disksBGDegrade[disksBGDegrade<0] = 0
#disksBGDegrade = uint8(disksBGDegrade)

#saveImage(disksFGDegrade, 'disksFGDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(disksBGDegrade, 'disksBGDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-non-flat \ se-flat
#disksDegradeNoiseB = bHMT(disksDegradeNoise, disksFG, disksBG)
#saveImage(ianeg(uint8(disksDegradeNoiseB)), 'disksDegradeNoiseB', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-non-flat \ se-non-flat
#disksDegradeNoiseBDegrade = bHMT(disksDegradeNoise, disksFGDegrade, disksBGDegrade)
#saveImage(ianeg(uint8(disksDegradeNoiseBDegrade)), 'disksDegradeNoiseBDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')


##RGHMT 
#disksFG = iasedisk()
#disksBG = ianeg(iasedisk())
#saveImage(iaseshow(bool_(disksFG), 'expand')*255, 'disksRG1FG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
#saveImage(iaseshow(bool_(disksBG), 'expand')*255, 'disksRG1BG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

#disksFGDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
#disksBGDegrade = openImage('G:\\Felipe\\Mestrado\\ArtificialImages\\diskDegradeRaio15.png')
#disksBGDegrade = int16(disksBGDegrade) - 50
#disksBGDegrade[disksBGDegrade<0] = 0
#disksBGDegrade = uint8(disksBGDegrade)

##IMG-non-flat \ se-flat
#disksDegradeNoiseRG = rgHMT(disksDegradeNoise, disksFG, disksBG)
#saveImage(ianeg(uint8(disksDegradeNoiseRG)), 'disksDegradeNoiseRG', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')

##IMG-non-flat \ se-non-flat
#disksDegradeNoiseRGDegrade = rgHMT(disksDegradeNoise, disksFGDegrade, disksBGDegrade)
#saveImage(ianeg(uint8(disksDegradeNoiseRGDegrade)), 'disksDegradeNoiseRGDegrade', 'G:\\Felipe\\Mestrado\\ArtificialImages\\SEsflat\\output')
##############RUIDOS FIM DISCOS GRADIENT