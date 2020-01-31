import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelBinarizer

from scipy import stats

def scale_numeric(X):
    X_num = X.select_dtypes(exclude='object')
    
    ss = StandardScaler()
    
    X_num_stand = pd.DataFrame(ss.fit_transform(X_num))
    X_num_stand.set_index(X.index, inplace=True)
    X_num_stand.columns = X_num.columns
    X_num_stand = X_num_stand[(np.abs(stats.zscore(X_num_stand)) < 2.5).all(axis=1)]
    
    return X_num_stand

def prepare_df(X,y):

    """
    parameters
    X: either X_train or X_test.

    returns
    scaled numeric values and encoded categorical variables
   
    """
    print(f'Before dropping duplicates and NAs across all columns {X.shape}')

    # Drop duplicates across all columns
    X.drop_duplicates(inplace=True)
    X.dropna(inplace=True)

    print(f'After dropping duplicates and NAs across all columns {X.shape}')
    
    X_numeric = scale_numeric(X)
    X_categorical = X.select_dtypes(include='object')

    # Scale numeric function removes outliers, so the line below matches
    # indices to maintain consistent shape of data
    X_categorical.loc[X_numeric.index]
    
    us_lb = LabelBinarizer()
    X_categorical["US"] = us_lb.fit_transform(X_categorical["US"])
    urb_lb = LabelBinarizer()
    X_categorical["Urban"]= urb_lb.fit_transform(X_categorical["Urban"])
    
    ohe = OneHotEncoder(sparse=False, drop='first')
    oh_features = pd.DataFrame(ohe.fit_transform(X_categorical[['ShelveLoc']]))
    oh_features.columns = list(ohe.categories_[0])[1:]
    oh_features.index = X_categorical.index

    X_categorical.drop('ShelveLoc', axis=1, inplace=True)
    X_categorical = X_categorical.join(oh_features)

    X = X_numeric.join(X_categorical)

    # make X and y have the same number of records
    y = y.loc[X.index]

    return X, y
   






    
    pd.get_dummies(X_)

    X = X_numeric.join(X_categorical, how='left' )

    

    return X

