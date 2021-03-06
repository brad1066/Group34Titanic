# -*- coding: utf-8 -*-
"""Titanic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wmgASSC4bXIgMKLE0SvPHo9xXxxRnaAH

**Importing necessary libraries**

I will import every library in the cell bellow to keep it organized
"""

'''Data manipulation and analyisis'''
import pandas as pd     # File read & write operation

'''Visualization'''
import seaborn as sns   # For plots and charts

'''Machine Learning'''
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC

"""**Importing the data**"""

#Importing CSV files
train_data = pd.read_csv('/content/train.csv')   #This file includes the survived column and we'll use it to trainthe AI
test_data = pd.read_csv('/content/test.csv')     #This file doesn't include the survived field, as that's what we're predicting with our machine learning model

"""**Exploring the data**"""

#Printing the list of columns in our files 
print(train_data.info())
print('\n\n')
print(test_data.info())

# Missing values
print('\nMissing values in trained data:')
print(train_data.isnull().sum())
print('\nMissing values in test data:')
print(test_data.isnull().sum())

#As you can see, there is missing data.
#I'm writing a function that shows the percentage of null values so we can visualize it better

def missing_data(df):
    total=df.isnull().sum().sort_values(ascending=False)
    percentage=round(total*100/len(df),2)
    return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])

print('The percentage of missing values in train data:')
display(missing_data(train_data))
print('\n\nThe percentage of missing values in test data:')
display(missing_data(test_data))

"""**Observations:**

-*We don't even have data about the cabins about a quarter of the people*

-*We're missing the age for 20% of the passagers*

  As we don't have enough data about the cabins and we concluded it's not influencing the outcome in any meaningful way, it will be removed.

  We believe age is relevant for the survival rate (we know women and children were prioritized), so I'll fill the missing fields with an average value.

**Dealing with missing data**
"""

#Removing the cabin column
train_data.drop('Cabin',axis=1,inplace=True)
test_data.drop('Cabin',axis=1,inplace=True)

#I'm plotting the age vs the passanger class:
sns.set_style("whitegrid")
sns.boxenplot(x="Pclass", y="Age", data=train_data)
#You can see that younger people are travelling in the lower classes.

#Finiding the average age for each class

def average_age(c):  
  age = train_data.groupby('Pclass')['Age'].mean()
  if c == 1: return round(age[1])
  if c == 2: return round(age[2])
  return round(age[3])
#This method returns the average age for a class number passed as an argument

#Impute a mean age based on the class of each passanger

def impute_age():
  train_data.loc[(train_data['Age'].isna()) & (train_data['Pclass'] == 1), 'Age'] = average_age(1)
  train_data.loc[(train_data['Age'].isna()) & (train_data['Pclass'] == 2), 'Age'] = average_age(2)
  train_data.loc[(train_data['Age'].isna()) & (train_data['Pclass'] == 3), 'Age'] = average_age(3)

  test_data.loc[(test_data['Age'].isna()) & (test_data['Pclass'] == 1), 'Age'] = average_age(1)
  test_data.loc[(test_data['Age'].isna()) & (test_data['Pclass'] == 2), 'Age'] = average_age(2)
  test_data.loc[(test_data['Age'].isna()) & (test_data['Pclass'] == 3), 'Age'] = average_age(3)

#Filling the missing fields in the 'Age' column with the average of each class

display(missing_data(train_data))

impute_age()

print('\n')
display(missing_data(train_data))

#Filling the missing fare values with the price that occurs most frequently
train_data['Fare'].fillna(train_data['Fare'].mode()[0],inplace=True)
test_data['Fare'].fillna(test_data['Fare'].mode()[0],inplace=True)

#Filling the missing values for Embarked with the most common port
train_data['Embarked'].fillna(train_data['Embarked'].mode()[0],inplace=True)
test_data['Embarked'].fillna(test_data['Embarked'].mode()[0],inplace=True)

display(missing_data(train_data))
print('\n')
display(missing_data(test_data))

"""**Feature Engineering**"""

pd.get_dummies(train_data['Embarked'],drop_first=True).head()
pd.get_dummies(test_data['Embarked'],drop_first=True).head()
sex_1=pd.get_dummies(train_data['Sex'],drop_first=True)
embark_1=pd.get_dummies(train_data['Embarked'],drop_first=True)
sex_2=pd.get_dummies(test_data['Sex'],drop_first=True)
embark_2=pd.get_dummies(test_data['Embarked'],drop_first=True)
train_data.drop(['Name','Sex','Ticket','Embarked'],axis=1,inplace=True)
test_data.drop(['Name','Sex','Ticket','Embarked'],axis=1,inplace=True)
train_data=pd.concat([train_data,sex_1,embark_1],axis=1)
test_data=pd.concat([test_data,sex_2,embark_2],axis=1)

"""**Preparing the data for machine learning**"""

y_train=train_data['Survived']
x_train=train_data.drop('Survived',axis=1)
x_test=test_data
print(x_train)

"""**Logistic Regression**"""

logreg=LogisticRegression()
logreg.fit(x_train,y_train)
y_pred_lr=logreg.predict(x_test)
accuracy_logistic=logreg.score(x_train, y_train)
print('Accuracy score by using logistic regression is:',round(accuracy_logistic,2))

"""**Random Forrest**"""

rf = RandomForestClassifier(n_estimators=100)
rf.fit(x_train, y_train)
y_pred_rf = rf.predict(x_test)
accuracy_randomforest=rf.score(x_train, y_train)
print('Accuracy score by using Random forest is:',round(accuracy_randomforest,2))

"""**Decision Tree**"""

dtc = DecisionTreeClassifier()
dtc.fit(x_train, y_train)
y_pred_dt = dtc.predict(x_test)
accuracy_decision=dtc.score(x_train, y_train)
print('Accuracy score by using Decision tree is:',round(accuracy_decision,2))

"""**Gaussian naive Bayes**"""

gaussian = GaussianNB()
gaussian.fit(x_train, y_train)
y_pred_gn = gaussian.predict(x_test)
accuracy_gaussian=gaussian.score(x_train, y_train)
print('Accuracy score by using Gaussian is:',round(accuracy_gaussian,2))

"""**Support Vector Machines**"""

svc=SVC()
svc.fit(x_train,y_train)
y_pred_sv=svc.predict(x_test)
accuracy_svc=svc.score(x_train, y_train)
print('Accuracy score by using SVM is:',round(accuracy_svc,2))

"""**K-Nearest Neighbor**"""

knn = KNeighborsClassifier(n_neighbors = 3)
knn.fit(x_train, y_train)
y_pred_kn = knn.predict(x_test)
accuracy_knn=knn.score(x_train, y_train)
print('Accuracy score by using KNN is:',round(accuracy_knn,2))

"""**Sumbmitting predictions**"""

#Exporting a CSV with the predictions from each model used

#Logistic regression
submission=pd.DataFrame({'PassengerId':test_data['PassengerId'],'Survived':y_pred_lr})
submission.to_csv('Logistic_regression.csv',index=False)

#Random forrest
submission=pd.DataFrame({'PassengerId':test_data['PassengerId'],'Survived':y_pred_rf})
submission.to_csv('Random_Forest.csv',index=False)

#Decision Tree
submission=pd.DataFrame({'PassengerId':test_data['PassengerId'],'Survived':y_pred_dt})
submission.to_csv('Decision_Tree.csv',index=False)

#Gaussian naive Bayes
submission=pd.DataFrame({'PassengerId':test_data['PassengerId'],'Survived':y_pred_gn})
submission.to_csv('Gaussian_naive_Bayes.csv',index=False)

#Support Vector Machines
submission=pd.DataFrame({'PassengerId':test_data['PassengerId'],'Survived':y_pred_sv})
submission.to_csv('Support_Vector_Machines.csv',index=False)

#K-Nearest Neighbor
submission=pd.DataFrame({'PassengerId':test_data['PassengerId'],'Survived':y_pred_kn})
submission.to_csv('K-Nearest_Neighbor.csv',index=False)

print("Predictions exported")