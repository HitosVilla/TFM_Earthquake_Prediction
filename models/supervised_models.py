def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from models import common


class Supervised(object):
    """ Base class to evaluate a models """

    def __init__(self, features, label):

        # Create logger
        self.logger = common.get_logger('SUP')

        # Initialize self variables for data
        self.features = features
        self.label = label

        # Split data into train and test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(features, label, test_size=0.20)

        self.logger.info('Initialized Supervised class. Data split into Train, Test\n')

    def evaluate_best_model(self, models):
        """ Evaluate different models to choose the best one

            :param models: should be Dict {ModelName: (Model, Parameter grid to be evaluated)}
            :return: best model, evaluated with GridSearchCV
        """

        models_grid_search = {}
        for name in models:
            model, parameter_grid = models[name]
            # Evaluate best parameters for each model
            self.logger.info('{}, Parameters Grid Search: {}'.format(name, parameter_grid))

            if name == 'LogisticRegression':
                metric = self.cross_validation(model, 5, 'accuracy')
                models_grid_search[name] = (max(metric), model, None)
            else:
                models_grid_search[name] = self.grid_search(model, parameter_grid)
                self.logger.info('Output: Score {} Parameter {} \n'.format(models_grid_search[name][0],
                                                                           models_grid_search[name][2].values()))
        best_model = min(models_grid_search.items(), key=lambda x: x[1][0])
        self.logger.info('BEST MODEL: {}'.format(best_model))

        return best_model

    def cross_validation(self, model, n, metric):
        """
        Call sklearn.model_selection.cross_val_score and return best_metric
        :param model: model to be evaluated
        :param n: Determines the cross-validation splitting strategy
        :param metric: name of the metric to evaluate mmodel
        :return: best_metric
        """
        # Calculate metrics for n subsets
        self.logger.info('Init Cross validation')
        best_metric = cross_val_score(model, self.features, self.label, cv=n, scoring=metric)
        self.logger.info('Model: {}, Best Metric {}: {}\n'.format(model, metric, best_metric))
        return best_metric

    def grid_search(self, model, param_grid_dict):
        """
        Call sklearn.model_selection.GridSearchCV and fit it.
        :param model: to be evaluated
        :param param_grid_dict: to evaluate
        :return: best score, best estimator and best params
        """

        model_test = GridSearchCV(model, param_grid=param_grid_dict, cv=5)
        model_test.fit(self.features, self.label)

        return model_test.best_score_, model_test.best_estimator_, model_test.best_params_
