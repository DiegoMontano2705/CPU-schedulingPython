from tabulate import tabulate
from itertools import islice
from queue import Queue

# Define clase Proceso
class Proceso:
  # Constructor de la clase Proceso
  def __init__(self, tiempoLlegada, pid, quantum):
    self.pid = pid # Almacena el id del proceso
    self.tiempoLlegada = tiempoLlegada # Almacena el tiempo en que llega el proceso a memoria
    self.quantum = quantum # Almacena el valor del quantum restante para cuando está en CPU
    self.estatus = 1 # Almacena el estatus que tiene un proceso (0-bloqueado, 1-listo, 2-corriendo, 3-terminado)
    self.tiempoEspera = 0 # Almacena el tiempo de que permanece en espera en cola de listos y en bloqueados
    self.tiempoCPU = 0 # Almacena el tiempo que toma correr en CPU
    self.tiempoTerminado = int() # Almacena el tiempo en que termina un proceso
    self.tiempoRetorno = int() # Almacena el tiempo que tarda en ser completado un proceso (tiempoTerminado-tiempoLlegada)
    self.interrupciones = Queue(maxsize=0)
  
  # Actualiza el valor del tiempoTermina de un proceso
  def setTermina(self, tiempoTerminado):
    self.tiempoTerminado = tiempoTerminado
    self.tiempoRetorno = tiempoTerminado - self.tiempoLlegada

  # Agrega I/O a cola de interrupciones
  def addInterrupcion(self, tiempo, comienzaIO):
    self.interrupciones.put((tiempo, comienzaIO))

  # Método para correr el proceso en CPU
  def corre(self):
    self.esatus = 2
    self.tiempoCPU = self.tiempoCPU + 1

  # Método para terminar un (I/O)
  def listo(self, queueListos):
    self.estatus = 1

  # Método para bloquear un proceso (I/O) 
  def bloqueado(self, queueBloqueado):
    self.estatus = 0

  # Método para terminar proceso
  def termina(self, tiempoTerminado, queueTerminados):
    self.estatus = 3

  # Muestra el contenido de objeto Proceso, función para debuggear
  def show(self):
    print("pid:{}\ntiempoLlegada:{}\nquantum:{}\nestatus:{}\ntiempoEspera:{}\ntiempoCPU:{}\ntiempoTerminado:{}\ntiempoRetorno:{}\ncolaInterrupciones:{}\n".format(self.pid, self.tiempoLlegada, self.quantum, self.estatus, self.tiempoEspera, self.tiempoCPU, self.tiempoTerminado, self.tiempoRetorno, self.interrupciones))

print('**** Bienvenido a CPU Scheduling Simulator ****')

# Pide nombre de archivo a leer y lo almacena en variable
# archivoLog = input('Ingresa el nombre del archivo de entrada con el log del sistema que deseas simular:\n')

# Crea objeto para acceder al contenido de un archivo
with open('rrEntrada.txt', "r") as archivoEntrada:

  # Lee la política del archivo (primera línea)
  politica = archivoEntrada.readline().strip().split()[0]
  
  # Valida que el archivo de entrada sea de FCFS o RR
  if politica != 'RR' and politica != 'FCFS':
    print('Al equipo solo le tocó simular FCFS y RR')
    exit()

  # Si el log es de RR
  if politica == 'RR':
    # Saca quantum y lo almacena en variable
    quantum = int(archivoEntrada.readline().strip().split()[1])

    # Diccionario que almacena los procesos
    Diccionario = {} 

    # Diccionario que almacena los procesos termiandos
    DiccionarioTermiandos = Queue(maxsize=0)

    # Crea las colas de listos, bloqueados y terminados que utilizará el simulador
    listos = Queue(maxsize=0)
    bloqueados = Queue(maxsize=0)
    terminados = Queue(maxsize=0)

    # Recorre el resto del archivo (a partir de la tercera línea)
    for linea in archivoEntrada:
      # Elimina el \n de la línea y la separa por palabras
      linea = linea.strip().split()
      tiempo = int(linea[0]) # Toma el timestamp
      accion = str(linea[1]) # Toma la acción
      # Si no se ha terminado la simulación
      if accion != "endSimulacion": 
        pid = int(linea[2]) # Toma el process ID
        
        # Llega un proceso
        if accion == 'Llega': 
          p = Proceso(tiempo, pid, quantum)
          Diccionario[pid] = p
        # Acaba un proceso
        elif accion == 'Acaba':
          Diccionario[pid].setTermina(tiempo)
        # Comienza un I/O
        elif accion == 'startI/O':
          # Agrega interrupción a la cola de interrupciones, true-startI/O
          Diccionario[pid].addInterrupcion(tiempo, True)
        # Termina un I/O
        elif accion == 'endI/O':
          # Agrega interrupción a la cola de interrupciones, false-endI/O
          Diccionario[pid].addInterrupcion(tiempo, False)
      else:
        pid = len(Diccionario)+1
        p = Proceso(tiempo,pid,0)
        Diccionario[pid] = p

# Cierra archivo
archivoEntrada.close()

# Contadores usados en CPU
contador = 1 # Lleva la cuenta de los procesos dentro del simulador de CPU (while)
relojCPU = 0 # Lleva la cuenta del tiempo dentro del siumulador del CPU
#Variables usadas de CPU
idProcesoEnCPU = int() # Almacena el id del proceso que se encuentra corriendo
eventoRealizado = str() # Almacena el string del evento en CPU




# Ciclo donde se simula el CPU , este acabada hasta que ya no hayan procesos en el Diccionario
while  relojCPU <= Diccionario[len(Diccionario)].tiempoLlegada:
  
  # Valida si el tiempo de CPU es igual al tiempo de llegada del proceso que está por llegar
  if relojCPU == Diccionario[contador].tiempoLlegada:
    print("proceso {} creado\n".format(contador))
    imprimirTabla = True
    # Guarda el ID del proceso en la cola de listos
    listos.put(Diccionario[contador].pid)
    # Valida si no hay proceso en CPU, pone el primer proceso de la cola de listos en el CPU
    if idProcesoEnCPU == None:
      idProcesoEnCPU = listos.get()
    contador = contador + 1
  
  # Ciclo para revisar si el tiempo de CPU es igual al tiempo de termiancion de un proceso
    for i in range(1,len(Diccionario)+1):
      if Diccionario[i].tiempoTerminado == relojCPU and Diccionario[i].estatus == 2:
        #Enciende variable para marcar el termino de un proceso
        pTerminado = True
        numeroProcesoTerminado = i
    pTerminado = False
    numeroProcesoTerminado = i

  # Valida si el tiempo de CPU es igual al tiempo de acabado de algun proceso 
  if pTerminado and numeroProcesoTerminado == idProcesoEnCPU:
    # Guarda el proceso en la cola de termiandos
    terminados.put(idProcesoEnCPU)
    # Cambia el status  del proceso a terminado
    Diccionario[idProcesoEnCPU].estatus = 3

  #Validación de Start I/O





  if imprimirTabla:
    # Crea tabla y la imprime 
    table = [["Test", "1", "2", "3", "4"]]
    print(tabulate(table,headers=[" Evento "," Cola de listos ", " CPU ", " Bloqueados ", " Termiandos "], tablefmt="fancy_grid"))
    imprimirTabla = False

  # Aumenta un milisegundo el reloj 
  relojCPU = relojCPU + 1
###