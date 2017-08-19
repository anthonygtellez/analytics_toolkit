#!/usr/bin/env python
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import RandomizedLogisticRegression as _RandomizedLogisticRegression
from base import BaseAlgo, ClassifierMixin
from codec import codecs_manager
from util import df_util
from util.param_util import convert_params, is_truthy
class RandomizedLogisticRegression(ClassifierMixin, BaseAlgo):
    def __init__(self, options):
        self.handle_options(options)
        self.estimator = _RandomizedLogisticRegression(random_state=None)
    def fit(self, df, options):
        # Make a copy of data, to not alter original dataframe
        X = df.copy()
        # Ensure there aren't too many classes
        df_util.limit_classes_for_classifier(X, self.target_variable)
        # Use all the variables
        used_variables = self.feature_variables + [self.target_variable]
        X, y, self.columns = df_util.prepare_features_and_target(
            X=X,
            variables=used_variables,
            target=self.target_variable,
        )
        # Encode the target
        self.label_encoder = LabelEncoder()
        encoded_y = self.label_encoder.fit_transform(y.values)
        # Fit the estimator
        self.estimator.fit(X.values, encoded_y)
        # Save the classes
        self.classes = np.unique(y)
    def apply(self, df, options):
        return df
    def summary(self, options):
        features = self.feature_variables
        scores = self.estimator.scores_
        return pd.DataFrame(zip(features, scores), columns=["feature", "score"])
    @staticmethod
    def register_codecs():
        from codec.codecs import SimpleObjectCodec
        codecs_manager.add_codec('atk_algos.RandomizedLogisticRegression', 'RandomizedLogisticRegression', SimpleObjectCodec)
        codecs_manager.add_codec('sklearn.linear_model.randomized_l1', 'RandomizedLogisticRegression', SimpleObjectCodec)
        codecs_manager.add_codec('sklearn.preprocessing.label', 'LabelEncoder', SimpleObjectCodec)
        codecs_manager.add_codec('sklearn.externals.joblib.memory', 'Memory', SimpleObjectCodec)
