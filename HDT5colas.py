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

# proceso principal del simulador

def proceso(enviroment, InstLL, CMemory, Memoria, CPU, WTime, CRandom):
    global SimuladorT, SimuladorDEV #simulador para controlar el tiempo de ejecucion
    #enviroment como tiempo actual
    NProcess = enviroment.now
    #contro de la RAM
    DispoRAM = Memoria.capacity - CMemory
    print('P: %7.4fs %s: Proceso/Llegada inst >>' % (NProcess, InstLL))
    print('P: %7.4fs %s: RAM req %s / RAM dis  %s' % (NProcess, InstLL, CRandom, DispoRAM)) 
    # Obtiene la RAM y usa el control
    with Memoria.get(CMemory) as MemoUS:     
        yield MemoUS
        EsperaT = enviroment.now - NProcess  # tiempo de espera, se incia proceso y se pide RAM      
        
        print('P: %7.4fs %s: Event: Ready >> Request RAM %6.3f' % (NProcess, InstLL, Memoria.level))
        # control de instrucciones de proceso
        while CRandom > 0:
            with CPU.request() as reqCPU: # Request para el CPU
                yield reqCPU
                print('P: %7.4fs %s: Running Event %6.3f' % (NProcess, InstLL, CRandom))

                yield enviroment.timeout(1)
                # Interrupt de los procesos en caso necesro 
                if CRandom > 3:
                    CRandom = CRandom - 3
                else:
                    CRandom = 0
            # control del proceso segun valores dados
            if CRandom > 0:
                PROWait = random.randint(1,2) # numero aleatorio para ver si espera o la inst se termina
                if PROWait == 1: # condiciones de que pasa si sale 1 , es decir que debe esperar
                    with WTime.request() as TMRequest: 
                        yield TMRequest #se solicita tiempo de espera
                        print ('P: %7.4fs %s: Waiting... >>' % (NProcess, InstLL))

                        yield enviroment.timeout(1)
              # fin de instrucciones
                print('P: %7.4fs %s: Ready >> Continue >>' % (NProcess, InstLL))

        # tempo del proceso atualmente
        ProcTime = enviroment.now - NProcess
        print ('p: %7.4fs %s:INST Terminada, ExecutionT >> %s' % (enviroment.now, InstLL, ProcTime))
	# RAM disponible	
        with Memoria.put(CMemory) as RefreshRAM:
            yield RefreshRAM
            print ('P: %7.4fs %s: Liberando RAM %s' % (enviroment.now, InstLL, CMemory))
	# Tiempo en ejecucion del simulador		
        SimuladorT = SimuladorT + (enviroment.now - NProcess)
        SimuladorDEV = (SimuladorT*SimuladorT) + (SimuladorDEV)
        print('P: %7.4fs Memoria utilizada / Revision RAM%6.3f >> tiempo Actual %s' % (enviroment.now, Memoria.level, SimuladorT))        

# se incia la simulacion del sistema operativo
print('>> System.Start <<')
random.seed(RANDOM_SEED)
enviroment = simpy.Environment()

# Ejecutar los procesos del sistema de simulacion 
CPU = simpy.Resource(enviroment, capacity=1)
Memoria = simpy.Container(enviroment, init=100, capacity=100)
WTime = simpy.Resource(enviroment, capacity=1)
enviroment.process(generador(enviroment, CREATE_PROCESS, INTERVALO_PRO, Memoria, CPU, WTime))
SimuladorT = 0
SimuladorDEV = 0
enviroment.run()
print "Tiempo de Ejecucion: " , SimuladorT, ": Promedio tiempo: " , SimuladorT/CREATE_PROCESS, ": Desviacion Estandar: " , ((SimuladorDEV/CREATE_PROCESS)**(0.5))

       
            
           
