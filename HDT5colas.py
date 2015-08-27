# Universidad del valle de Guatemala
#Algoritmos y estructura de datos
# Alejandro de Leon 14345 , Yasmin Valdez 14079
# Hoja de trabajo # 5 
# Se utilizo como referencia ejemplos vistos en clase

# se importan las clases 
import random
import simpy

# P se refiere al proceso

#declaracion de variables para control de ejecuccion de procesos
RANDOM_SEED = 42
CREATE_PROCESS = 150
INTERVALO_PRO = 10.0 

# genera procesos con lo requisitos planteados en la hoja de trabajo
def generador(enviroment, NumPro, intervalo, Memoria ,CPU, WTime):
    for i in range(NumPro):
        #Aleatorios de instrucciones y de memoria 
        CRandom = random.randint(1,10) 
        CMemory = random.randint(1,10) 
        Generator = proceso(enviroment, 'Proceso:%02d' % i, CMemory, Memoria ,CPU, WTime, CRandom)
        enviroment.process(Generator)
        timeSimulator = random.expovariate(1.0 / intervalo) 
        yield enviroment.timeout(timeSimulator)


