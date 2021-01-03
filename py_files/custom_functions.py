import numpy as np
import scipy.stats as sp
import seaborn as sns

def mean_by_pos(df,stat):
    '''this function takes a dataframe and a statistic as an argument and returns
    the correlation between the statistic and the logged transfer fee 
    overall and subset by the aggregate position as well as a 
    scatterplot hued by position'''
    a1r, a1p = sp.pearsonr(df[stat],df['fee_final_logged'])
    att = df.loc[df['position_agg'] == 'attacker']
    def_ = df.loc[df['position_agg'] == 'defender']
    mid = df.loc[df['position_agg'] == 'midfielder']
    ar, ap = sp.pearsonr(att[stat],att['fee_final_logged'])
    br, bp = sp.pearsonr(mid[stat],mid['fee_final_logged'])
    cr, cp = sp.pearsonr(def_[stat],def_['fee_final_logged'])
    print(f'overall correlation of {stat} with fee: r={np.round_(a1r, 3)}, p={np.round_(a1p, 3)}')
    print(f'correlation of {stat} with fee for attackers: r={np.round_(ar, 3)}, p={np.round_(ap, 3)}')
    print(f'correlation of {stat} with fee for midfielders : r={np.round_(br, 3)}, p={np.round_(bp,3)}')
    print(f'correlation of {stat} with fee for defenders: r={np.round_(cr,3)}, p={np.round_(cp,3)}')
    return sns.scatterplot(data=df, x=stat,y='fee_final_logged', hue='position_agg');

import numpy as np
from sklearn import metrics

def model_evaluation(model, X_train, X_test,y_train, y_test):
    '''This function takes as an arugment a model that has already
    been fit (to accomodate difference in fitting of OLS and gridsearching
    ridge and lasso).  Note that should be fed the fit linear model or the 
    appropriate "model.best_estimator_" for grid searched models.  Additionally
    takes in the train and test X and y values to facilitate use with polynomials
    and PCA.  
    Returns the train and test adjusted R^2 and RMSE'''
    #predict on the training and test set (modeled log of fee as outcome)
    log_y_train_pred = model.predict(X_train)
    log_y_test_pred = model.predict(X_test)

    #exponentiate the predicted values
    y_train_pred = np.exp(log_y_train_pred)
    y_test_pred = np.exp(log_y_test_pred)

    #calculate RMSE on exponentiated predicted and exponentiated y values to get RMSE in pounds
    train_rmse = np.sqrt(metrics.mean_squared_error(np.exp(y_train), y_train_pred))
    test_rmse = np.sqrt(metrics.mean_squared_error(np.exp(y_test), y_test_pred))
    
    print(f'Model eval for: {model}')
    print('Training adj R squared:', round(model.score(X_train, y_train),3))
    print('Training Root Mean Squared Error:' , round(train_rmse,3))
    print('Testing adj R squared:', round(model.score(X_test, y_test),3))
    print('Testing Root Mean Squared Error:' , round(test_rmse,3))


def lin_reg(X_train, X_test, y_train, y_test):
    '''This function takes as an input the train test split on X and Y and returns the 
    RMSE and adj R2 for the training and testing data.  This is built specifically for
    the ln of the transfer fee given the findings in EDA of the dist of fee'''
    #instantiate a linear regression object
    lm = LinearRegression()

    #fit the linear regression to the data
    lm = lm.fit(X_train, y_train)

    #predict on the training and test set (modeled log of fee as outcome)
    log_y_train_pred = lm.predict(X_train)
    log_y_test_pred = lm.predict(X_test)

    #exponentiate the predicted values
    y_train_pred = np.exp(log_y_train_pred)
    y_test_pred = np.exp(log_y_test_pred)

    #calculate RMSE on exponentiated predicted and exponentiated y values to get RMSE in pounds
    train_rmse = np.sqrt(metrics.mean_squared_error(np.exp(y_train), y_train_pred))
    test_rmse = np.sqrt(metrics.mean_squared_error(np.exp(y_test), y_test_pred))

    print('Training adj R squared:', round(lm.score(X_train, y_train),3))
    print('Training Root Mean Squared Error:' , round(train_rmse,3))
    print('Testing adj R squared:', round(lm.score(X_test, y_test),3))
    print('Testing Root Mean Squared Error:' , round(test_rmse,3))