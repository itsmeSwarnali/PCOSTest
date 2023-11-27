import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, plot_roc_curve, classification_report, accuracy_score 
from sklearn.ensemble import RandomForestClassifier

X_train = np.load('Saved Model/X_train.npy')
X_test = np.load('Saved Model/X_test.npy')
y_train =np.load('Saved Model/ytrain.npy')
y_test = np.load('Saved Model/ytest.npy')


loaded_rf_model = pickle.load(open('Saved Model/final_rf_model.pkl', 'rb'))
loaded_rf_model = loaded_rf_model.score(X_test, y_test)*100
print(loaded_rf_model)

#creating picle object
#@pickle.dump(rf, open('cardio.pkl','wb'))



