from sklearn.model_selection import train_test_split, cross_val_score

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor


class Supervised(object):
    """ Base class to evaluate a models """

    def __init__(self, features, label):

        # Initialize variables
        self.model_name = ''
        self.best_metric = 0
        self.model_test = ''

        # Initialize data
        self.features = features
        self.label = label

        # Split data into train and test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(features, label, test_size=0.10)

    def cross_validation(self, model, n, metric):
        # Calculate metrics for n subsets
        best_metric = cross_val_score(model, self.features, self.label, cv=n, scoring=metric)

        return best_metric

    def grid_search(self, model, param_grid_dict):
        # Search for the best parameters
        model_test = GridSearchCV(model, param_grid=param_grid_dict)
        model_test.fit(self.features, self.label)

        return model_test.best_score_, model_test.best_estimator_, model_test.best_params_

    def evaluate_best_regression_model(self):

        regression_linear = LinearRegression()
        regression_linear.fit(self.X_train, self.y_train)

        regression_k = KNeighborsRegressor(n_neighbors=2)
        regression_k.fit(self.X_train, self.y_train)

        regression_tree = DecisionTreeRegressor(max_depth=3)
        regression_tree.fit(self.X_train, self.y_train)

        regression_forest = RandomForestRegressor(n_estimators=100, max_depth=10, min_samples_leaf=20)
        regression_forest.fit(self.X_train, self.y_train)
        # Gradient Boosting Tree

    def evaluate_best_classification_model(self):

        classification_logistic = LogisticRegression()
        classification_logistic.fit(self.X_train, self.y_train)

        classification_k = KNeighborsClassifier(n_neighbors=2)
        classification_k.fit(self.X_train, self.y_train)

        classification_tree = DecisionTreeClassifier(min_samples_leaf=20, max_depth=3)
        classification_tree.fit(self.X_train, self.y_train)

        classification_svc = SVC(kernel="linear", C=10)
        classification_svc.fit(self.X_train, self.y_train)

        classification_forest = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=20)
        classification_forest.fit(self.X_train, self.y_train)

        gbr = GradientBoostingRegressor(max_depth=4, n_estimators=100, learning_rate=0.1)
        cross_val_score(gbr, self.features, self.label, scoring='neg_mean_absolute_error').mean()


