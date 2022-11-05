import numpy as np
import functionsMaths as f
from data_functions import generar_data_letras, distorsionar_letras, get_letras

class Perceptron(object):
    def __init__(self, sizes, aprendizaje, momento):

        self.sizes = sizes
        self.aprendizaje = aprendizaje
        self.momento = momento
        self.cant_capas = len(sizes) + 2
    
    def init_params(self):
        w = []
        b = []
        w1 = np.random.rand(self.sizes[0], 100)
        b1 = np.random.rand(1, self.sizes[0])[0]

        if len(self.sizes) == 2:

            w2 = np.random.rand(self.sizes[1], self.sizes[0])
            w3 = np.random.rand(3, self.sizes[1])
            b2 = np.random.rand(1, self.sizes[1])[0]
            b3 = np.random.rand(1, 3)[0]
            w.append(w1)
            w.append(w2)
            w.append(w3)
            b.append(b1)
            b.append(b2)
            b.append(b3)


        elif len(self.sizes) == 1:
            w2 = np.random.rand(3, self.sizes[0])
            b2 = np.random.rand(1, 3)[0]
            w.append(w1)
            w.append(w2)
            b.append(b1)
            b.append(b2)

        self.w = w
        self.b = b
        return w, b
    
    def init_layers(self):
        capa_entrada = np.zeros(100, dtype=int)
        capa_salida = np.zeros(3, dtype=float)
        capas_ocultas = []

        for i in range(len(self.sizes)):
            capa_oculta = np.zeros(self.sizes[i])
            capas_ocultas.append(capa_oculta)
        
        capas = [capa_entrada, *capas_ocultas, capa_salida]
        self.capas = capas
        return capas

    def feedforward(self, x, w, b):
        cant_capas = self.cant_capas #4
        z = [x]
        y = [x] 
        for i in range(cant_capas-1):
            #0 ,1, 2
            yi = []
            zi = []
            for j in range(len(w[i])):
                #Suma ponderada
                entrada = np.dot(y[i],w[i][j])
                #Funcion de activacion
                if i == cant_capas - 2:
                    salida = f.sigmoide(entrada+b[i][j])
                else:
                    salida = f.lineal(entrada+b[i][j])
                zi.append(entrada)
                yi.append(salida)
            y.append(np.array(yi))
            z.append(np.array(zi))
        
        
            
        return y


    def backpropagation(self, ye, y, w):
        #Ye: es la salida espera
        #A: vector de salidas de activacion --> se podria eliminar y pasar solo la salida
        #W: pesos de las capas
        #Delta de capa de salida
        deltas = []
        delta_out = f.derivate_error(ye,y[-1])*f.derivate_sigmoide(y[-1])
        delta_out = np.array(delta_out)
        deltas.append(delta_out)
        for wi in reversed(w):
            delta=[]
            wt = np.transpose(wi)
            for i in range(len(wt)):
                delta.append(np.sum(wt[i]*deltas[-1])*f.derivate_lineal())
            deltas.append(delta)
            #deltaInput =np.array(delta)
        
    
        return list(reversed(deltas))

    def gradiente_descendente(self, w, deltas, y):
        
        
        #Backforward

        for i in range(len(w)-1, -1, -1):
            for j in range(len(w[i])):
                if i>0:
                    for k in range(len(w[i-1])):
                        w[i][j][k] -= y[i][j]*deltas[i][j]*0.3
                    
                else:
                    for k in range(100):
                        w[i][j][k] -= y[i][j]*deltas[i][j]*0.3
        return w
            
    """ def predict(self, letra):
        letra = ["b","d","f"]
        porcentaje = 0
    
        for i in range(self.cant_capas-1):
            yi = []
            zi = []
            for j in range(len(w[i])):
                #Suma ponderada
                entrada = np.dot(y[i],w[i][j])
                #Funcion de activacion
                if i == self.cant_capas - 2:
                    salida = f.sigmoide(entrada+b[i][j])
                else:
                    salida = f.lineal(entrada+b[i][j])
                zi.append(entrada)
                yi.append(salida)
            y.append(np.array(yi))
            z.append(np.array(zi))
        

        return y """

    def train(self, data_train):
        #Dividiendo data train en una tupla (entrada,clase)
        er = np.array([0,0,0])
        letras_train = []
        for letra in data_train:
            x_train = letra[:100]
            y_train = letra[100:]
            letras_train.append((x_train, y_train))

        w = self.w
        b = self.b
        err = []
  
        for e in range(50):
            np.random.shuffle(letras_train)
            for i in range(len(letras_train)):

                
                #Con feedforward obtengo la salida de todas las capas
                y = self.feedforward(letras_train[i][0], w, b)
                #!!-----Calculo del error-----!!!
                
                #La salida obtenida
                y_obtenido = y[-1]

                #La salida esperada
                ye = np.array(letras_train[i][1])

                #La sumatoria de errores

                er = np.sum([er, (ye-y_obtenido)**2], axis=0)
                #----------------------------------------------------#

                #BACKPROPAGATION le paso la salida esperada, las salidas de las capas y los pesos a partir de la segunda capa
                deltas = self.backpropagation(ye, y, w[1:])
                #Backforward
                #w_prueba = w.copy()

                #Gradiente descendiete: Le paso los pesos, los deltas y las salidas de las capas
                w = self.gradiente_descendente(w, deltas, y[1:])
                #print(w_prueba[2])
                #len w[2] = 3
                #len w[1] = 5
                        
                

            er = er/(2*len(letras_train))
            err.append(er)

        self.w = w
        self.b = b

        letra = ["b","d","f"]
        porcentaje = 0 
        cant=0
        
        for i in range(len(letras_train)):
            y = self.feedforward(letras_train[i][0], self.w, self.b)
            salida = np.zeros_like(y[-1])
            salida = y[-1]

            
        
        
        for e in err:
            print(np.mean(e))





cantidad = "100"
letras = get_letras(cantidad)
data_train = letras[:int(len(letras)*0.8)]
data_test = letras[int(len(letras)*0.8)+1:int(len(letras)*0.8)+int(len(letras)*0.15)]
data_validation = letras[int(len(letras)*0.8)+int(len(letras)*0.15)+1:99]



perceptron = Perceptron([5,5], 0.3, 0.2)
w, b = perceptron.init_params()
capas = perceptron.init_layers()


perceptron.train(data_train)

clases = {
    'b': [1, 0, 0],
    'd': [0, 1, 0],
    'f': [0, 0, 1]
}

""" letra = "b"
distorsion = 0.2
codificar_letra(letra) """
