import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import preprocessing
import unitycommunication.unity_comm as unitycomm
import time

numero_voluntario = 1

# Reading data
print('[INFO] Lendo dados...')
caminho_dados = '../data/processado/volunteer_' + str(numero_voluntario) + '_processed.csv'
dataset = pd.read_csv (caminho_dados, sep=',')

X = dataset.iloc[:, [x for x in range(0,26)]].values
y = dataset.iloc[:, -1].values

# Splitting data by output5
#movimentos = {}
#for i in range(1,7):
#    movimentos[i] = dataset[dataset.output == i]
    
    
# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting classifier to the Training set
clf = SVC(kernel='linear', random_state=0, decision_function_shape='ovo')
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)


# Predicting the Test set results
lin, = y_test.shape
y_pred = np.zeros((lin,1))

time.sleep(4)

for i in range(0,lin):
    y_pred[i] = clf.predict([X_test[i,:]])
    unitycomm.relay_movement_command(int(y_pred.item(i)))
    prever_proximo = str(input(">>>> Prever próxima movimento? [Y/n] " ))
    
    print(prever_proximo)
    if not (prever_proximo == '' or prever_proximo.lower() == 'y'):
        break
#    time.sleep(4)



# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

