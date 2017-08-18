#!/usr/bin/env python

import json

from algos.LogisticRegression import LogisticRegression
from sklearn.linear_model import LogisticRegression as _LogisticRegression
from util.param_util import convert_params, is_truthy
from codec import codecs_manager


from cexc import get_messages_logger
messages = get_messages_logger()


class MultinomialLogisticRegression(LogisticRegression):
    def __init__(self, options):
        self.handle_options(options)

        out_params = convert_params(
            options.get('params', {}),
            bools=['fit_intercept', 'probabilities'],
            strs=['solver', 'multi_class', 'class_weight']
        )

        # Solver
        if 'solver' in out_params:
            if out_params['solver'] not in ['newton-cg', 'lbfgs']:
                raise RuntimeError('solver must be either: newton-cg or lbfgs')
        else:
            # default
            out_params['solver'] = 'newton-cg'

        # Multiclass
        if 'mutli_class' in out_params:
            if out_params['multi_class'] not in ['ovr', 'multinomial']:
                raise RuntimeError('multi_class must be either: ovr or multinomial')

        if 'class_weight' in out_params:
            try:
                weights = out_params['class_weight'].replace('\'', '"')
                out_params['class_weight'] = json.loads(weights)
            except Exception:
                s = """Example: class_weight="{'field_one': 0.3, 'field_two': 0.7}"""
                messages.error("Unable to load class_weight dictionary. Are field names correct? %s" % s)
                messages.warn("Setting class_weight to 'balanced'.")
        else:
            out_params['class_weight'] = 'balanced'

        if 'probabilities' in out_params:
            del out_params['probabilities']

        self.estimator = _LogisticRegression(**out_params)

    def fit(self, df, options):
        try:
            super(MultinomialLogisticRegression, self).fit(df, options)
        except TypeError:
            messages.error("""Class weight value:  %s \n
            Example: class_weight="{'Some Field': 0.3, 'other_field_name': 0.7}" """
                           % self.estimator.class_weight)
            raise RuntimeError("""Unable to initialize algorithm. This is most
            likely due to missing class values or misspelled field names.""")


    @staticmethod
    def register_codecs():
        from codec.codecs import SimpleObjectCodec
        codecs_manager.add_codec('algos.MultinomialLogisticRegression', 'MultinomialLogisticRegression', SimpleObjectCodec)
        codecs_manager.add_codec('sklearn.linear_model.logistic', 'LogisticRegression', SimpleObjectCodec)
