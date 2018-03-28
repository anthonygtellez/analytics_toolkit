from base import BaseAlgo
from util.param_util import convert_params
from sklearn.preprocessing import PolynomialFeatures as _PolynomialFeatures
from pandas import DataFrame
import numpy as np

class PolynomialFeatures(BaseAlgo):
    """Generate polynomial and interaction features"""
    def __init__(self,options):
        """Check the options supplied""" 
        self.feature_variables = options.get('feature_variables', {})
        target_variable = options.get('target_variable', {})

        if len(self.feature_variables) == 0:
            raise RuntimeError('You must supply one or more fields')

        if len(target_variable) > 0:
            raise RuntimeError('PolynomialFeatures does not support the from clause')

        params = options.get('params', {})
        out_params = convert_params(
            params,
            ints=['degree'],
            bools=['interaction_only','include_bias'])
        self.preprocessor = _PolynomialFeatures(**out_params)

    def get_feature_names(self, input_features=None):
        # not available in this version of scikit-learn, backport from current
        # https://github.com/scikit-learn/scikit-learn/blob/a24c8b46/sklearn/preprocessing/data.py#L1265
        """
        Return feature names for output features
        Parameters
        ----------
        input_features : list of string, length n_features, optional
            String names for input features if available. By default,
            "x0", "x1", ... "xn_features" is used.
        Returns
        -------
        output_feature_names : list of string, length n_output_features
        """
        powers = self.preprocessor.powers_ # this is the only line that was changed, from self -> self.preprocessor
        if input_features is None:
            input_features = ['x%d' % i for i in range(powers.shape[1])]
        feature_names = []
        for row in powers:
            inds = np.where(row)[0]
            if len(inds):
                name = " ".join("%s^%d" % (input_features[ind], exp)
                                if exp != 1 else input_features[ind]
                                for ind, exp in zip(inds, row[inds]))
            else:
                name = "1"
            feature_names.append(name)
        return feature_names

    def fit(self,df,options):
        """Compute the polynomial features and return a DataFrame"""
        requested_columns = df[self.feature_variables]
        output_df = DataFrame(self.preprocessor.fit_transform(requested_columns), columns = self.get_feature_names(requested_columns.columns))
        return output_df
