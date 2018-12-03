# Load the Pandas libraries with alias 'pd'
import pandas as pd

data = pd.read_csv("train.csv")
testData = pd.read_csv("test.csv")

# Preview the first 5 lines of the loaded data
#print(data.head(5))
#data.describe()


# test and training datasets are already split
train_features = data.iloc[:,:294]
train_labels = data.iloc[:,-6:]

test_features = testData.iloc[:,:294]

#print(train_features)
#print(train_labels)


# Reverse OneHotEncoder
train_labels = pd.DataFrame(train_labels)
train_labels=pd.DataFrame(train_labels.values, columns = list('abcdef'))
train_labels = train_labels.idxmax(1)

#print(train_labels)


# Classification using Support Vector Machine
from sklearn import svm
clf = svm.SVC(gamma=0.001, C=100.)
clf.fit(train_features, train_labels)
df = pd.DataFrame(clf.predict(test_features))
print(df.shape)


# Convert into one hot Encoder again
one_hot = pd.get_dummies(df)#.to_string(header=False)
# print(one_hot.shape)

# Merge with test data
test_features = pd.DataFrame(test_features)
print(test_features.shape, one_hot.shape)


frames = [test_features, one_hot]
result = pd.concat(frames, sort=False, ignore_index=True, axis=1)
result.to_csv('out.csv', index=False, header=False)
