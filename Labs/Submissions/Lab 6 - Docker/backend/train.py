from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_and_save():
    iris = load_iris()
    X, y = iris.data, iris.target

    clf = RandomForestClassifier(n_estimators=50)
    clf.fit(X, y)

    joblib.dump(clf, "model.joblib")

if __name__ == "__main__":
    train_and_save()
