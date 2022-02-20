import math
from random import randint
import time
import random 
import numpy
import matplotlib.pyplot as plt     #kniznica na tvorenie grafu

def generuj_suradnice(pocet_miest):         #generovanie súradnic x,y pre dané mestá
    mesta = []
    for i in range(pocet_miest):
        mesto = []
        x = randint(0,200)                  #generovanie suradnice x z intervalu 0,200
        y = randint(0,200)                  #generovanie suradnice y z intervalu 0,200
        mesto.append(x) 
        mesto.append(y)
        mesta.append(mesto)                 #append mesta do skupiny miest
    return mesta

def vzdialenost(mesto1,mesto2):               #funkcia na výpočet vzdialenosti 2 miest na "mape" (pomocou pytagorovej vety)
    return math.sqrt(abs(mesto1[0] - mesto2[0])**2 + (abs(mesto1[1] - mesto2[1])**2))

def fitness(cesta,mesta):                   #funkcia na výpočet hodnoty cesty 
    cesta_cost = 0
    for i in range(len(cesta)):
        if(i+1!=len(cesta)):
            cesta_cost = cesta_cost + vzdialenost(mesta[cesta[i]],mesta[cesta[i+1]])
        else:
            cesta_cost = cesta_cost + vzdialenost(mesta[cesta[i]],mesta[cesta[0]])
    return cesta_cost

def swap(cesta):                                    #funkcia na vymenu hodnoty na dvoch random indexoch v ceste
    cesta_opt = []
    init_cesta = cesta.copy()
    for i in range(100):
        cesta=init_cesta.copy()
        ran1 = randint(1, len(cesta)-1)
        ran2 = randint(1, len(cesta)-1)
        while(ran1==ran2):
            ran1 = randint(1, len(cesta)-1)
            ran2 = randint(1, len(cesta)-1)
        cesta[ran1], cesta[ran2] = cesta[ran2], cesta[ran1]
        cesta_opt.append(cesta)
    return cesta_opt

def simulated_annealing(pocet_miest, mesta):
    cesta = []
    for i in range(pocet_miest):
        cesta.append(i)
    min_path = cesta.copy()
    t_count = 0
    T = 50                     #pociatocna teplota
    factor = 0.99               #faktor zmensenia teploty 
    cesta_opt = []
    while(t_count<500):
        T=T*factor
        cesta_opt = swap(min_path)
        for option in cesta_opt:
            cesta_cost = fitness(option, mesta)
            min_cost = fitness(min_path, mesta)
            if(cesta_cost < min_cost):
                min_path=option.copy()
                min_cost = cesta_cost
                t_count=0
            else:
                x=numpy.random.uniform()                #vygenerovanie cisla 0-1
                if x < numpy.exp((min_cost-cesta_cost)/T):   
                    min_cost = cesta_cost
                    min_path = option.copy()
                    t_count=0
                else:
                    t_count = t_count+1
            #print(min_cost)
    return min_cost, min_path

def graf(cesta, init_cesta, mesta):     #pomocna funkcia na vykreslenie grafu
    x = []
    y = []
    init_x = []
    init_y = []
    for i in range(len(cesta)+1):
        if(i!=len(cesta)):
            x.append(mesta[cesta[i]][0])
            y.append(mesta[cesta[i]][1])
            init_x.append(mesta[init_cesta[i]][0])
            init_y.append(mesta[init_cesta[i]][1])
        else:
            x.append(mesta[cesta[0]][0])
            y.append(mesta[cesta[0]][1])
            init_x.append(mesta[init_cesta[0]][0])
            init_y.append(mesta[init_cesta[0]][1])
    fig, axs = plt.subplots(2)
    axs[0].plot(init_x,init_y, marker = 'o', color='blue')
    axs[1].plot(x,y, marker = 'o', color='red')
    fig.suptitle("Simulated Annealing")
    plt.show()

def main():
    pocet_miest = randint(20,40)            #vygenerovanie poctu miest
    mesta=generuj_suradnice(pocet_miest)    #vygenerovanie suradnic pre mesta
    init_cesta=[]
    for i in range(pocet_miest):            #vygenerovanie cesty ku mestam 
        init_cesta.append(i)                
    print("Povodna cesta: ",init_cesta)
    print("Povodna vzdialenost: ",fitness(init_cesta,mesta))
    start_time = time.time()                #zapnutie casu
    distance,cesta = simulated_annealing(pocet_miest,mesta)
    print("Finalna cesta: ",cesta)
    print("Finalna vzdialenost: ",distance)
    print("Cas: ",time.time()-start_time)
    graf(cesta,init_cesta,mesta)

main()



    