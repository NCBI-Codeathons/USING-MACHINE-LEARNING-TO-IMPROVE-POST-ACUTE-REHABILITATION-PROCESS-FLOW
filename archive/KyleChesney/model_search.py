# This is my preliminary search for promising ML models made on the night of 11/9/2019
# Also contained are functions to visualise decision boundaries
from sklearn.datasets import make_blobs
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn import preprocessing
from sklearn import svm
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

LE = preprocessing.LabelEncoder()
OH = preprocessing.OneHotEncoder()

# actual data
df = pd.read_csv('data/IRF_data.csv')
df = df.dropna(how='any', axis=0)
df = df.apply(preprocessing.LabelEncoder().fit_transform)
Y = df.y_actual # ground truth is bin of onset days
X = df.drop('y_actual', axis=1)

classes = Y.unique()

X = preprocessing.StandardScaler().fit_transform(X)
x_train, x_test, y_train, y_test = sk.model_selection.train_test_split(X, Y)

def confusion_matrix(y_true, y_pred, classes, normalize = False, cmap = plt.cm.plasma):
    cm = sk.metrics.confusion_matrix(y_true, y_pred)
    classes = classes[sk.utils.multiclass.unique_labels(y_true, y_pred)]
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap = cmap)
    ax.figure.colorbar(im, ax = ax)
    ax.set(xticks=np.arange(cm.shape[1]),
            xticklabels = classes,
            yticklabels = classes,
            yticks=np.arange(cm.shape[0]),
            title='confusion matrix',
            ylabel='True label',
            xlabel='Predicted label')
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax

# Trying to create a custom visually appealing, colorblind friendly cmap
# using UTSW/UF colors to pander
top = plt.cm.get_cmap('Oranges_r', 128)
middle = plt.cm.get_cmap('Greens_r', 128)
bottom = plt.cm.get_cmap('Blues', 128)
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
newcolors = np.vstack((
            top(np.linspace(0, 1, 128)),
            middle(np.linspace(0, 1, 128))
            bottom(np.linspace(0, 1, 128))
            ))
OrBu = ListedColormap(newcolors, name='OrBu')

# using a cusom arg for cmap doesn't actually work(?)
def decision_boundary(X, y, clf, step_size = 0.02, cmap = plt.cm.viridis):
    PCA = sk.decomposition.PCA(n_components = 2)
    PCA_X = PCA.fit_transform(X)
    X1 = PCA_X[:, 0]
    X2 = PCA_X[:, 1]
    x_min, x_max = X1.min() - .5, X1.max() + .5
    y_min, y_max = X2.min() - .5, X2.max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, step_size),
                         np.arange(y_min, y_max, step_size))
    fig, ax = plt.subplots()
    clf.fit(PCA_X, y)
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha = 0.5, cmap = cmap)
    ax.scatter(X1, X2, c=y, cmap = cmap)
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_xticks(())
    ax.set_yticks(())
    return ax

def decision_boundary_3d(X, y, clf):
    PCA = sk.decomposition.PCA(n_components = 3)
    PCA_X = PCA.fit_transform(X)
    clf.fit(PCA_X, y)
    X1 = PCA_X[:, 0]
    X2 = PCA_X[:, 1]
    X3 = PCA_X[:, 2]
    fig, ax = plt.subplots()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X1, X2, X3)
    plt.show()

RF = RandomForestClassifier()
LR = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
SVM = svm.SVC(decision_function_shape='ovo')
NN = MLPClassifier()

RF.fit(x_train, y_train)
LR.fit(x_train, y_train)
SVM.fit(x_train, y_train)
NN.fit(x_train, y_train)

decision_boundary(X, Y, RF)
plt.show()

# ?
decision_boundary_3d(X, Y, RF)

RF.score(x_test, y_test)
LR.score(x_test, y_test)
SVM.score(x_test, y_test)
NN.score(x_test, y_test)

confusion_matrix(y_test, LR.predict(x_test), classes = classes, normalize = True, cmap = plt.cm.PuRd)
plt.show()


