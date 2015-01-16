import os
import cPickle as pkl
from matplotlib.pyplot import *

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.grid_search import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier, LogisticRegression,\
        LinearRegression, Ridge, Lasso
from sklearn.feature_selection import SelectKBest
from sklearn.svm import SVC, LinearSVC, SVR
from sklearn.preprocessing import StandardScaler
from sklearn import base


class ColumnSelectTransformer(base.BaseEstimator, base.TransformerMixin):
    """
    Transformer to select only particular columns from a dataset.
    """
    def __init__(self, columns=[], astype=None):
        self.columns = columns
        self.astype = astype
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        if self.astype is None:
            return X[:,self.columns]
        else:
            return X[:,self.columns].astype(self.astype)

class EstimatorTransformer(base.BaseEstimator, base.TransformerMixin):
    """
    Wrap an estimator so that its transform function mirrors the predictor.
    """
    def __init__(self, estimator=None):
        self.estimator = estimator
    def fit(self, X, y=None):
        self.estimator.fit(X, y)
        return self
    def transform(self, X):
        return self.estimator.predict(X).reshape(-1, 1)
    def _get_param_names(self):
        return ['estimator']


def column_locs(df, columns):
    """
    Find and return the index of each of the named columns.
    """
    return [df.columns.get_loc(c) for c in columns]


def select_data(df, balance=True):
    """
    Select a subset of the data where the outcomes of all loans is essentially
    known. Optionally balance the data to have as many failed loans as
    successful.
    """
    comp = df[df.completed]
    if balance:
        num_use = min(len(comp[comp.failed].index),
            len(comp[~comp.failed].index))
        return comp.ix[
            comp[comp.failed][:num_use].index.union(
                comp[~comp.failed][:num_use].index)]
    else:
        return comp


def featurize(df, params={}, fit=True, 
        columns=['subgrade_code', 'annual_inc', 'total_acc', 'revol_bal'],
        text_trans=Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('kbest', SelectKBest(k=1000))])):
    """
    Convert a data-frame's descriptions to text features, extract a set of
    numeric columns, and return the result as a matrix.
    Also return a vector indicating whether each loan has not yet failed.
    (1 = no failure yet, 0 = loan has failed)
    """ 
    y = ~df.failed.reshape(-1)
    if fit:
        text_trans.set_params(**params)
        text_trans.fit(df.desc.apply(str), y)
    textdat = text_trans.transform(df.desc.apply(str))
    data = df[columns].fillna(-1).as_matrix().astype(float)
    alldata = concatenate((data, textdat.todense()), axis=1)
    return alldata, y
