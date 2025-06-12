import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split
from sklearn_extensions.extreme_learning_machines.elm import GenELMClassifier
from sklearn_extensions.extreme_learning_machines.random_layer import RBFRandomLayer, MLPRandomLayer
from sklearn.metrics import accuracy_score 
from numpy.linalg import norm
from numpy import dot
import imutils

files = []
filename = 'data/Fake'
label = []
for root, dirs, directory in os.walk(filename):
    for i in range(len(directory)):
        files.append(filename+"/"+directory[i]);
        label.append(0)

filename = 'data/Real'
for root, dirs, directory in os.walk(filename):
    for i in range(len(directory)):
        files.append(filename+"/"+directory[i]);
        label.append(1)

print(len(files))
X = np.ndarray(shape=(len(files), 16384), dtype=np.float32)
Y = np.ndarray(shape=(len(files)),dtype=np.float32)
print(X.shape)
print(Y.shape)
for i in range(len(files)):
    img = cv2.imread(files[i])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img,(128,128))
    img = img.reshape(-1)
    X[i] = img
    Y[i] = label[i]

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.1, random_state = 0)
print(X_train.shape)
print(y_train.shape)
print(y_train)

def prediction(X_test, cls): 
    y_pred = cls.predict(X_test) 
    for i in range(len(X_test)):
      print("X=%s, Predicted=%s" % (X_test[i], y_pred[i]))
    return y_pred 
	
# Function to calculate accuracy 
def cal_accuracy(y_test, y_pred): 
    accuracy = accuracy_score(y_test,y_pred)*100
    return accuracy

def get_pixel(img, center, x, y):
    new_value = 0
    try:
        if img[x][y] >= center:
            new_value = 1
    except:
        pass
    return new_value

def lbp_calculated_pixel(img, x, y):
    center = img[x][y]
    val_ar = []
    val_ar.append(get_pixel(img, center, x-1, y+1))     # top_right
    val_ar.append(get_pixel(img, center, x, y+1))       # right
    val_ar.append(get_pixel(img, center, x+1, y+1))     # bottom_right
    val_ar.append(get_pixel(img, center, x+1, y))       # bottom
    val_ar.append(get_pixel(img, center, x+1, y-1))     # bottom_left
    val_ar.append(get_pixel(img, center, x, y-1))       # left
    val_ar.append(get_pixel(img, center, x-1, y-1))     # top_left
    val_ar.append(get_pixel(img, center, x-1, y))       # top
    
    power_val = [1, 2, 4, 8, 16, 32, 64, 128]
    val = 0
    for i in range(len(val_ar)):
        val += val_ar[i] * power_val[i]
    return val    


srhl_tanh = MLPRandomLayer(n_hidden=500, activation_func='tanh')
cls = GenELMClassifier(hidden_layer=srhl_tanh)
cls.fit(X_train, y_train)
prediction_data = prediction(X_test, cls) 
elm_acc = cal_accuracy(y_test, prediction_data)
print(elm_acc)

img_bgr = cv2.imread('testimages/fake.jpg')
height, width, channel = img_bgr.shape
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
img_lbp = np.zeros((height, width,3), np.uint8)
for i in range(0, height):
    for j in range(0, width):
        img_lbp[i, j] = lbp_calculated_pixel(img_gray, i, j)
cv2.imwrite('test.jpg', img_lbp)

img1 = cv2.imread('test.jpg')
img1 = cv2.resize(img,(128,128))
img1 = img1.reshape(-1)
y_pred = cls.predict(img1)
print(len(y_pred))
print(y_pred)

img_bgr = cv2.imread('testimages/real.jpg')
height, width, channel = img_bgr.shape
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
img_lbp = np.zeros((height, width,3), np.uint8)
for i in range(0, height):
    for j in range(0, width):
        img_lbp[i, j] = lbp_calculated_pixel(img_gray, i, j)
cv2.imwrite('test1.jpg', img_lbp)

img1 = cv2.imread('test1.jpg')
img1 = cv2.resize(img,(128,128))
img1 = img1.reshape(-1)
y_pred = cls.predict(img1)
print(len(y_pred))
print(y_pred)

    
