import time
import math
import sys
from random import shuffle

#Clase base para los nodos
class Node:
#Constructor de la clase
    def __init__(self,state, parent, operator,depth):
        self.state=state
        self.parent=parent
        self.operator=operator
        self.depth=depth

#Funcion para crear nodos
def create_node(state,parent,operator,depth):
    return Node(state,parent,operator,depth)

#Función que define los limites del tablero para saber hasta que punto se puede mover cada ficha segun su posicion
def limits(size):
    limit={"up":[i for i in range(size)],
    #El limite superior son las primeras n posiciones, donde n es el tamaño del lado
            "right":[i*size-1 for i in range(1,size+1)],
    #El limite derecho son n*1-1,..., n*n-1
            "down":[i for i in range((size**2)-size,size**2)],
    #El limite inferior son los ultimos n numeros de n^2-1
            "left":[i*size for i in range(size)]
    #El limite izquierdo son los numeros iniciando con 0 1*n hasta n*(n-1)
    }
    #Devuelve un diccionario con los limites usando la palabra del limite deseado en ingles como llave
    return limit

#Función que establece un diccionario a forma de hash_table para guardar los estados visitados
def set_hash(size):
    #recibe como parametro el tamaño para generar todas las posibles posiciones donde puede estar el vacio
    dicts={}
    i=0
    for i in range(size**2):
    #ciclo que va de 0 hasta (n^2)-1 para llenar el diccionario con las posiciones posibles
        dicts[i]=[]
    return dicts

#Función que establece el tamaño del tablero
def board_size():
    return int(input("Tamaño de lado del tablero: "))

#Función que establece el estado inicial mediante la entrade de usuario
def set_initial(size):
    state=[]
    print("Ingrese los numeros del tablero inicial en orden izquierda a derecha:")
    for n in range(size**2):
        r=int(input("Elemento en "+str(n+1)+": "))
        state.append(r)
    return state

#Función que establece el estado objetivo basado en el tamaño del tablero y la posicion donde se desea que esté el vacio
def set_goal(size,option):
    goals={
        "normal":[n for n in range(1,size**2)]+[0], #objetivo 123...0
        "arriba":[n for n in range (size**2)]       #objetivo 012...n^2 donde n es el tamaño del lado del tablero
    }
    return goals.get(option) #regresa el estado objetivo deseado


def random_state(size):
    t=[n for n in range(size**2)] 
    shuffle(t)
    show(t,size)
    return t

#Funcion que define el movimiento del espacio vacio hacia arriba
def move_up(state,limits):
    new_state=state[:] #realiza una copia del estado recibido
    index=new_state.index(0)  #busca el indice del espacio vacio en el estado
    limit=limits["up"] #define el limite superior
    size=limit[-1] #obtiene el tamaño-1 del lado obteniendo la ultima posicion del arreglo
    if index not in limit: #si la posicion del vacio no esta en el borde superior
        temp=new_state[index-(size+1)] #obtiene el valor del numero arriba del espacio vacio
        new_state[index-(size+1)]=new_state[index] #cambia el valor del vacio con el valor que estaba arriba de el
        new_state[index]=temp #pone el valor que estaba arriba del vacio donde estaba el vacio
        return new_state
    else:
        return None #si esta en el limite regresa None

def move_down(state,limits):
    new_state=state[:]
    index=new_state.index(0)
    limit=limits["down"]
    size=limit[-1]
    if index not in limit:
        temp=new_state[index+int(math.sqrt(size+1))]
        new_state[index+int(math.sqrt(size+1))]=new_state[index]
        new_state[index]=temp
        return new_state
    else:
        return None

def move_left(state,limits):
    new_state=state[:]
    index=new_state.index(0)  
    if index not in limits["left"]:
        temp=new_state[index-1]
        new_state[index-1]=new_state[index]
        new_state[index]=temp
        return new_state
    else:
        return None

def move_right(state,limits):
    new_state=state[:]
    index=new_state.index(0)
    if index not in limits["right"]:
        temp=new_state[index+1]
        new_state[index+1]=new_state[index]
        new_state[index]=temp
        return new_state
    else:
        return None

#Funcion para verificar que un estado no regrese al estado que lo generó
def not_return(operator):
    dictionary={
        "\u2191":"\u2193", #arriba no regresa a abajo
        "\u2192":"\u2190", #derecha no regresa a izquierda
        "\u2193":"\u2191", #abajo no regresa a arriba
        "\u2190":"\u2192"  #izquierda no regresa a derecha 
    }
    return dictionary.get(operator)

#Funcion para verificar los estados visitados
def visited(state):
    index=state.index(0)   #obtiene la llave del hash que es la posicion del vacio
    if state in hash_table[index]: #si el estado ya ha sido visitado regresa verdadero
        return True
    return False #si no regresa falso

#funcion para guardar los estados visitados
def set_visited(state):
    #obtiene la llave del hash donde va a guardar
    index=state.index(0)
    #como modifica una variable fuera de su alcance debe usarse la palabra reservada global
    global hash_table
    #agrega el estado a la lista
    hash_table[index].extend([state])

#Funcion para expandir los nodos
def expand(node,nodes,size):
    succesors=[]
    l=limits(size) #genera los limites del tablero
    #crea los nuevos nodos a partir del nodo a expandir
    succesors.append(create_node(move_up(node.state,l),node,"\u2191",node.depth+1))
    succesors.append(create_node(move_left(node.state,l),node,"\u2190",node.depth+1))
    succesors.append(create_node(move_down(node.state,l),node,"\u2193",node.depth+1))
    succesors.append(create_node(move_right(node.state,l),node,"\u2192",node.depth+1))

    #elimina los estados no validos
    succesors=[node for node in succesors if node.state!=None]

    #para cada sucesor verifica que no regrese al estado que lo genero
    for s in succesors:
        if s.operator==not_return(node.operator):
            #si regresa lo saca de los sucesores
            succesors.pop(succesors.index(s))
    
    #verifica que los sucesores no contengan estados visitados
    for v in succesors:
        if visited(v.state)==True:
            #si ha sido visitado se elimina de la lista
            succesors.pop(succesors.index(v))

    for v in succesors:
        if v in nodes:
            succesors.pop(succesors.index(v))
    return succesors

#funcion de busqueda general
def general_search(initial,goal,qnf,size):
    start=time.time() #inicia a contar el tiempo
    memory=0
    extended=0
    nodes=[]
    #genera el nodo inicial
    strt=create_node(initial,None,None,0)
    nodes.append(strt) #lo agrega a la lista de nodos
    while True: #ciclo "incondicional"
        if len(nodes)==0: #si ya no hay nodos por expandir
            clear_hash()  #limpia el hash
            return None #regresa None
        node=nodes.pop(0)#saca el primer nodo en la lista
        memory += sys.getsizeof(node) #suma el tamaño del nodo a la memoria usada
        set_visited(node.state) #guarda el estado del nodo como visitado
        extended+=1
        if node.state==goal: # si el estado del nodo es el objetivo
            end=time.time()
            moves=[]
            temp=node #guarda el nodo solucion
            while True:
                moves.insert(0,temp.operator)#guarda el operador al inicio de la lista
                if temp.depth==1:# si la profundidad es igual a 1 
                    break   #sale del ciclo porque el padre no tiene operador, es el nodo inicial
                temp=temp.parent #obtiene el padre del temporal 
            move=""
            for m in moves:
                move+=(m+" ")
            print("Solución: ",len(moves)," movimientos")
            print(move)
            print("Nodos explorados: ",extended," Nodos en frontera: ",len(nodes)," Tiempo: ",round((end-start),20),'s'
                    , "Memoria: ",memory+sys.getsizeof(nodes),"bytes")
            clear_hash()
            return moves
        if qnf==at_front: #si la funcion de ordenacion de la lista es al frente (depth_first)
            if node.depth<50: #limite para evitar que genere soluciones de mas de mil movimientos
                nodes=qnf(nodes,expand(node,nodes,size)) #expande el nodo
        elif qnf==a_star_sort: #si es la ordenacion usando f(n)
            nodes=qnf(nodes,expand(node,nodes,size),goal,size) #expande los nodos, tiene diferente numero de parametros
        else:
            nodes=qnf(nodes,expand(node,nodes,size))

#elimina el hash para ser inicializado de nuevo
def clear_hash():
    global hash_table
    hash_table={ }

#Funcion para depth first
def dfs(initial,goal,size):
    return general_search(initial,goal,at_front,size)

#funcion para breadth first
def bfs(initial,goal,size):
    return general_search(initial,goal,at_end,size)

#funcion para limited depth first, se utiliza para iterativo
def ldfs(initial,goal,limit,size):
    clear_hash()
    start=time.time()
    nodes=[]
    extended=0
    global hash_table
    hash_table=set_hash(size)
    memory=0
    nodes.append(create_node(initial,None,None,0))
    while True:
        if len(nodes)==0:
            clear_hash()
            return None
        node=nodes.pop(0)
        memory+=sys.getsizeof(node)
        extended +=1
        set_visited(node.state)
        if node.state==goal:
            end=time.time()
            moves=[]
            temp=node
            while True:
                moves.insert(0,temp.operator)
                if temp.depth==1:
                    break
                temp=temp.parent
            move=""
            for m in moves:
                move+=(m+" ")
            print("Solución: ",len(moves)," movimientos")
            print(move)
            print("Nodos explorados: ",extended," Nodos en frontera: ",len(nodes)," Tiempo: ",round((end-start),10),'s ',"Memoria: ",memory+sys.getsizeof(nodes))
            clear_hash()
            return moves
        if node.depth<limit:
            nodes=at_front(nodes,expand(node,nodes,size))

#funcion para profundidad iterativa  
def ids(initial,goal,size):
    #establece el limite de profundidad segun entrada de usuario
    limit=int(input("Limite de profundidad: "))
    start=time.time()
    for i in range(limit):#iteraciones de 0 hasta limite -1
        r=ldfs(initial,goal,i,size)
        if r!=None: # si encuentra una solucion sale del ciclo
            end=time.time()
            print("Tiempo total: ",round(end-start,20))
            return r 
    end=time.time()
    #si no encuentra solucion
    print("Tiempo total: ",round(end-start,20))
    return None

#funcion de ordenamiento al final
def at_end(Li,li):
    Li.extend(li) #agrega varios elementos al final de la lista
    return Li

#funcion para ordenar al frente
def at_front(Li,li):
    for n in li: #para cada elemento en la lista 
        Li.insert(0,n) #inserta cada elemento al frente
    return Li

#funcion para obtener la distancia manhattan
def manhattan(state,goal,size):
    distance=0
    for i in range(len(state)): #por cada numero de 0 hasta n-1 donde n es el tamaño del lado del tablero
        #como es un arreglo unidimensional se deben sacar los valores de X y Y a partir del indice
        x=state.index(i)%size #con el modulo se sacan valores secuenciales hasta n-1 [0,1,2,...]
        y=state.index(i)//size #con division entera se saca el mismo valor para n valores consecutivos [0,0,0,1,...]
        x1=goal.index(i)%size
        y1=goal.index(i)//size
        t=abs(x-x1)+abs(y-y1) #ecuacion para distancia manhattan
        distance+=t #suma la distancia manhattan de cada cuadrito
    return distance

#Funcion para ordenar segun f(n)
def a_star_sort(Li,li,goal,size):
    for n in li: #para cada elemento en la lista  (sucesores)
        h=manhattan(n.state,goal,size) #obtiene h(n) de cada sucesor
        setattr(n,'cost',h+n.depth) #añade el atributo "cost" con el valor de h(n) + g(n) a cada nodo
        Li.append(n) #agrega el nodo a la lista de nodos
    Li.sort(key=lambda n : n.cost)   #ordena la lista de nodos segun f(n) ascendente
    return Li

#funcion para A*
def a_star(initial,goal,size):
   return general_search(initial,goal,a_star_sort,size)

#diccionario para mostrar los movimientos de la solucion
switch={
    "\u2191":move_up,
    "\u2192":move_right,
    "\u2193":move_down,
    "\u2190":move_left
} 

#funcion para mostrar los estados
def show(state,size):
    #comprension de lista. divide el estado en lineas del tamaño del lado del tablero
    l=[state[i:i + size] for i in range(0, len(state), size)]
    print("---------------")
    for n in l:     
        m=""
        for s in n:
            if s<10:
                m+=(" "+str(s)+" ")
            else:
                m+=(str(s)+" ")           
        print(m)
    print("---------------")

#funcion para seleccionar la estrategia de busqueda
def algorithm_option(option):
    options={
        "bfs":bfs,
        "ids":ids,
        "a*":a_star
    }
    return options.get(option)

#funcion main
def main():
    size=board_size()
    initial_state=set_initial(size)
    goal_state=set_goal(size,input("Seleccione objetivo: arriba | normal: ").lower())
    global hash_table
    hash_table=set_hash(size)
    algorithm=algorithm_option(input("Seleccione algoritmo de busqueda: BFS (Breadth-First) |"+
     "IDS (Iterative depth search) | A* ").lower())
    solution=algorithm(initial_state,goal_state,size)
    if solution!=None: #si tiene solucion
        s=initial_state
        show(s,size) #muestra el estado inicial
        l=limits(size)
        for m in solution:
            r=switch[m](s,l) #segun el operador realiza el movimiento del vacio y lo asigna a r
            show(r,size) #muestra el estado r
            s=r #asigna el estado a s para generar el siguiente movimiento
    else:
        print("No tiene solucion")
    
    print("¿Desea realizar una nueva busqueda?")
    resp=input("Si | No  \n").lower()
    if resp=="si":
        main()
    
if __name__ == "__main__":
    main()
