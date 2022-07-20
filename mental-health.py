# -*- coding: utf-8 -*-
"""Copy of MentalHealth.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JMrh821hKU2_kG7PCrZWepESO48RK5WL

# 1. Import Libraries
"""

import pandas as pd

"""# 2. Importing the Dataset"""

url = 'https://raw.githubusercontent.com/donSalieri-rgb/Mental-Health-Prediction/main/survey.csv'
data = pd.read_csv(url)

print(data.head())

"""# 3. Taking Care of Missing Values"""

#data.isnull() # Returns Boolena value True/False indicating the value is present or not.
data.isnull().sum() # Returns the sum of all True values indicating the number of values missing in an attribute.
data = data.dropna()
data.isnull().sum()

"""# 4. Taking Care of Duplicate Values"""

data_dup = data.duplicated().any() # Returns True if any duplicate value is present in the Dataset.
 data_dup

data = data.drop_duplicates() # This function drops all the duplicate values present in the Dataset.
data_dup = data.duplicated().any() # Check again if all duplicate values have been dropped or not.
data_dup

"""# 5. Data Processing"""

from sklearn import preprocessing
#Encode data in form of 1 and 0
labelDict={}
for feature in data:
    le = preprocessing.LabelEncoder()
    le.fit(data[feature])
    le_name_mapping = dict(zip(le.classes_,le.transform(le.classes_)))
    data[feature] = le.transform(data[feature])
    #Get Labels
    labelKey='label_'+feature
    labelValue=[*le_name_mapping]
    labelDict[labelKey]=labelValue

for key, value in labelDict.items():     
    print(key, value)

#Get rid of 'Country'
data = data.drop(['Country'], axis= 1)
data.head()

# First seperate categorical columns and numerical columns because we have to handle them seperately.
cate_val = [] # To store categorical columns.
cont_val = [] # To store numerical columns.

for column in data.columns:
  if data[column].nunique() <= 10:
    cate_val.append(column) # If there are less than 11 values in column then it can be considered in categorical column.
  else:
    cont_val.append(column) # If more than 10 unique values then in numerical column.

cate_val # All categorical colummns.

cont_val # All numerical columns.

"""# 6. Encoding Categorical Data"""

""" We will first create binary vectors for all the categorical columns. 
    The size of these binary vectors will depend on the number of unique values present in the respective column. These vectors will contain dummy variables.
    These dummy variables are not required for sex and target column as they have only two values.
    Because of these dummy variables we will have a problem called dummy variable trap, 
    in this scenario the independent variable are highly corelated meaning one variable can be predicted from others. 
    To remove this problem we remove the first column.
    Eg. for 'cp' column we have values [0,1,2,3] -: The binary vectors will be 
                                                    0 1 2 3
                                                    1 0 0 0
                                                    0 1 0 0
                                                    0 0 1 0
                                                    0 0 0 1
"""
pd.get_dummies(data,columns=cate_val,drop_first=True)

data.head() # To check the dummy variables formed.

""" As we can see from the table the values of the columns are not in the same scale.
    So thats why we require feature scaling.
    Feature Scaling is essential for ML Algorithms to calculate the distance between the data.
    If not done then values with high range start dominating.
    Algorithms that require feature scaling - K Nearest Neighbours, Neural Network, SVM, Linear Regression and Logistic Regression.
    Non linear ML Algortihms such as Random Forest, Decision Forest, Ada Boost, etc.
""" 
data.head()
#  Feature Scaling is not required for the encoded categorical columns.

"""# 7. Feature Scaling"""

from sklearn.preprocessing import StandardScaler # importing library

st = StandardScaler() # Instance of Standard Scaler
data[cont_val] = st.fit_transform(data[cont_val]) # Using function to transform all continous columns to same scale.

data.head() # Now we can see that all the values are in the same scale.

"""# 8. Splitting The Dataset Into The Training Set and Test Set"""

# We perform this step which later helps us in evaluating the performance of our ML Algorithms. 
# First seperate the independent variable and dependent variable.
X = data.drop('treatment',axis = 1) # Our dependent variable.
feature_cols = ['Age', 'Gender', 'family_history', 'benefits', 'care_options', 'anonymity', 'leave', 'work_interfere']
X = data[feature_cols]

X # Here you can see all the independent variables.

y = data['treatment'] # Our dependent variable.
y

# To perform Train/Test split we have to import library
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state = 42) # We create two set, one for training and one for test
# We set aside 20% data for testing purpose.

X_train # The training set containing independent variables.

X_test # The test set containing independent variables.

data.head()
# As we can see the target variable has 0/1 values so we find that this is a classification problem. So from here we will use classification algorithms.

from sklearn.linear_model import LogisticRegression # import library for Logisitc Regression Model.

"""# 9. Logistic Regression"""

log = LogisticRegression() # Instance of this Logisitic Regression.
log.fit(X_train,y_train) # Train our model.

y_pred1 = log.predict(X_test) # Perform prediction on unseen samples.

# Check the accuracy of the model.
from sklearn.metrics import accuracy_score # import library to check the accuracy.

accuracy_score(y_test, y_pred1)
# accuracy_score(actual_values , predicted values)

"""# 10. SVC"""

from sklearn import svm  # import library for Support Vector Machine.

svm = svm.SVC() # Instance for SVC

svm.fit(X_train,y_train) # Train our model.

y_pred2 = svm.predict(X_test) # Perform prediction on unseen samples.

accuracy_score(y_test, y_pred2)
# accuracy_score(actual_values , predicted values)

"""# 11. KNeighbors Classifier"""

from sklearn.neighbors import KNeighborsClassifier  # import library for KNeighbors Classifier.

knn = KNeighborsClassifier(n_neighbors = 4) # Instance for KNN

knn.fit(X_train,y_train) # Train our model.

y_pred3 = knn.predict(X_test) # Perform prediction on unseen samples.

accuracy_score(y_test, y_pred3)
# accuracy_score(actual_values , predicted values)

"""
  By default the number of neighbors in KNN is 5.
  So we try different number of neighbors and check for which value we 
  get the best accuracy.
  We store all the accuracy in score list.
"""

score = []

for k in range(1,40):
  knn = KNeighborsClassifier(n_neighbors = k)
  knn.fit(X_train,y_train)
  y_pred = knn.predict(X_test)
  score.append(accuracy_score(y_test, y_pred))

score # Here we can see that when we have 2 neighbors we get the best accuracy.

"""# 12. Non-Linear ML Algorithms

For Non-Linear ML Algorithms pre-processing is not required so we do not perfrom encoding and feature scaling.

url = 'https://raw.githubusercontent.com/donSalieri-rgb/Mental-Health-Prediction/main/survey.csv'
data = pd.read_csv(url)
data = data.drop('Timestamp',axis = 1)
"""

data.head()

data = data.drop_duplicates() # Removing all the duplicate values.

data.shape

feature_cols = ['Age', 'Gender', 'family_history', 'benefits', 'care_options', 'anonymity', 'leave', 'work_interfere']
X = data[feature_cols]
y = data['treatment']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2, random_state = 42)

"""# 13. Decision Tree Classifier"""

from sklearn.tree import DecisionTreeClassifier # import library for Decision Tree Classifier.

dt = DecisionTreeClassifier() # Instance of DecisionTreeClassifier.

dt.fit(X_train,y_train) # Train our model.

y_pred4 = dt.predict(X_test) # Perform prediction on unseen samples.

accuracy_score(y_test,y_pred4) # accuracy_score(actual_values , predicted values)

"""# 14. Random Forest Classifier

"""

from sklearn.ensemble import RandomForestClassifier #  Random Forest Classifier

rf = RandomForestClassifier() # Instance of DecisionTreeClassifier.

rf.fit(X_train,y_train) # Train our model.

y_pred5 = dt.predict(X_test) # Perform prediction on unseen samples.

accuracy_score(y_test,y_pred5) # accuracy_score(actual_values , predicted values)

"""# 15. Success method plot"""

final_data = pd.DataFrame({'Models' : ['LR','SVM','KNN','DT','RF'],
                           'ACC' : [accuracy_score(y_test,y_pred1),
                                    accuracy_score(y_test,y_pred2),
                                    accuracy_score(y_test,y_pred3),
                                    accuracy_score(y_test,y_pred4),
                                    accuracy_score(y_test,y_pred5)]})
                                    # accuracy_score(acutal value, predicted value)
# The performance of all the models is converted to a data frame using their accuracy score.

final_data

import seaborn as sns # Importing this libarary to visualise the success plot data frame.

sns.barplot(final_data['Models'],final_data['ACC'])

"""# 16. Train best model on entire dataset.

"""

log = LogisticRegression()
log.fit(X,y)

"""# 17. Prediction on New Data"""

feature_cols = ['Age', 'Gender', 'family_history', 'benefits', 'care_options', 'anonymity', 'leave', 'work_interfere']
new_data = pd.DataFrame({
    'Age':52, 
    'Gender': 0,
    'family_history':1, 
    'benefits': 1, 
    'care_options': 0, 
    'anonymity': 1, 
    'leave':0, 
    'work_interfere': 0
}, index = [0])

new_data

p = log.predict(new_data)
if p[0] == 0:
  print("Does not require Help")
else:
  print("Requires help")

"""# Deplyoment"""

pip install Flask

import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from sklearn.preprocessing import StandardScaler

pickle.dump(log, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb'))
print(model)
