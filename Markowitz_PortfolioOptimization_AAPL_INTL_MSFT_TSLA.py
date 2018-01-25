# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 09:35:30 2018

@author: Brandon O'Briant

The problem definition: 
    With new tech companies emerging everyday, which four companies should I
    build my Tech Portfolio with? Given those four choosen, how can I optimize
    this portfolio to maximize returns, while minimizing total cost?

Research:
    Using the same practices as Warren Buffet to choose his core holdings
    (foundation of a portfolio) of choosing long intrenched and strong core
    hodlings (i.e. Coca-cola, IBM, American Express). Since I am looking to 
    build a portfolio with tech based core holdings I am going to look at three
    which have been around for a while, building/inovating new
    tech that we use everyday, and have had a strong stable performance/growth 
    over time: Microsoft, Intel, and Apple Inc.
    
    For the fourth core holding I have choosen Tesla Inc, due to its prowess 
    in the new inovative auto technologies and that SpaceX is boosting reliability
    of Elon Musks tech muscles along with the fact that I cannot directly 
    invest in SpaceX yet and would have to invest in compaies that produce
    materials or are sending up sateliets and plan to use SpaceX to do it, I 
    believe that by investing in Tesla Inc, it will be the closet to gaining
    a reward from the performance of SpaceX. This is definitly a 10+ year 
    risk/reward investment. 
    
Solution:
    This program looks to analyis a portfolio built upon the core holdings of:
    Microsoft (MSFT), Apple Inc. (AAPL), Intel (INTC), and Tesla Inc. (TSLA).
    
    Then optimize this portfolio to produce the maximum return on my investment,
    while minimizing my total cost. 
    
    By calculating the rate of a return of a portfolio that contains these four
    secruities, we can find the histociral rate of return (expected rate) from 
    this portfolio in the future. 
    
    We will calculate the rates of return for each individual security and
    multiply this by the weight it has in the overall portfolio. 
        
        sum(rate of return for a security_i * weight in portfolio_i)
        for i = 1,...,4
    
    Fo an equally weighted portfolio, this would mean in our case that
    each stock has a weight of 25% since:
        
                     sum(APPL return * 25%,
                         MSFT return * 25%,
                         INTL return * 25%,
                         TSLA return * 25%)
                        
    The sum of these return would be the rate of the return for the portfolio.
    
    Since, we are looking to optimize our portfolio the weights will vary. The
    calculation will be the same, but will the different weights. For example,
    APPL 35%, MSFT 25%, INTL 15%, TSLA 25%:
              
                      sum(APPL return * 35%,
                          MSFT return * 25%,
                          INTL return * 15%,
                          TSLA return * 25%)
    
"""
# import packages to be used in the namespace
import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt



# overrides the default rcParams for plotting
def init_plotting():
    plt.style.use(style='ggplot')
    plt.rcParams['figure.figsize'] = (10.0, 8.0)
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['text.color'] = 'black'
    plt.rcParams['axes.labelcolor'] = 'black'
    plt.rcParams['xtick.color']= 'black'
    plt.rcParams['ytick.color']= 'black'
init_plotting()
# avoid empty plot, always good to close plot
plt.close() 


# note about numpy, we can vectorize (organize several knids of data processing
# tasks as array expression) data to simplify calucations
# using one or multi demensional arrays

# The adjusted closing price will be used for calucaltions in this program
# since the adjusted closing price (Adj Close) accounts for dividen payouts
# and stock splits

# ticker_df, desired name for pandas DataFrame
# tickername, type string, is the name of the ticker for source to look up
# data_source is yahoo
# start_date, the desired start date of the stock information
def import_stock_data(ticker_df, tickers, start_date):
    ticker_df = pd.DataFrame()
    for t in tickers:
        ticker_df[t] = wb.DataReader(t, data_source = 'yahoo',
                               start = start_date)['Adj Close']
    return ticker_df


# prints first and last few rows of DataFrame
# prints information about DataFrame (number of columns, rows, data type)
def print_head_tail_info_df(dataframe):
    print('\n{} first ten rows:\n {}'.format(dataframe.name, dataframe.head()))
    print('\n{} last ten rows:\n {}'.format(dataframe.name, dataframe.tail()))
    print('\n{} dataframe information:\n {}'.format(dataframe.name, dataframe.info()))

# start date for the stocks data
# the dataset starts June 29, 2010 and goes to present
s_d = '2010-6-29'

# tickers for stocks to be ustilized in this program
tickers = ['AAPL', 'MSFT', 'INTL', 'TSLA']

# port_data, pandas DataFrame to store stock data
# initialized to enmtpy DataFrame
port_data = pd.DataFrame()

# add name to DataFrame
port_data.name = 'portfolio'

# import the stock data from yahoo for the tickers, and store it in port_data
# ------NOTE: check this agains yahoo to make sure information is correct-----#
port_data = import_stock_data(port_data, tickers, s_d) 

# add name to DataFrame
port_data.name = 'portfolio'


# check the first and last few rows and infor for port_data
print_head_tail_info_df(port_data)


# Normalizatoin to 100: helps normalize data to 100
#  (P_t/P_0) * 100
# create subset of data using .iloc[0] to exract the data from the first column
# of the table to be used in normailization procedure to use for campring 
# all stocks as if they all started at 100
# create line chart of data to compare behavior of stocks
(port_data/port_data.iloc[0]*100).plot(figsize = (15,6))
plt.savefig('Line-Chart_Compare_Behvior.pdf', 
    bbox_inches = 'tight', dpi=None, facecolor='w', edgecolor='b', 
    orientation='portrait', papertype=None, format=None, 
    transparent=True, pad_inches=0.25, frameon=None)
plt.show()
plt.close()

##############################################################################
#            Calcualting The Return of Portfolio Securities                  #
##############################################################################
## Simple Rate of Return
# To calcualte the simple rate of return  we use todays
# closing price minus the previous days price all divided by the previous
# days closing price: 
#       (P_1 - P_0)/P_0
# Another way to express this is 
#         (P_1/P_0)-1

# calcualtes the simple rate of return
# creates a new column to store the simple_return
# returns dataframe with the new column associated with the simple rate of return
# we shift the day using pandas.DataFrame.shit(# of lags), in our case
# # of lags is 1, thus we are shifting the index by 1
# Note there will be a nan value for the first value, since there is no lag for the
# first day recorded
# prints out the calcualted results
def simple_rate_of_return(dataframe):
    returns = (dataframe/dataframe.shift(1)) -1
    print('\n{} simple_rate_of_return results:\n {}'
          .format(dataframe.name, returns))
    return returns

# calculate the portfolios annual returns with using simple return time 250
# then calcualte the expected return (annual) with dot product of weights
# and annual returns
def portfolio_annual_return_weights(simple_returns, weights):
        # calculate the annual return
        annual_returns = simple_returns.mean()*250
        # calulate portfolio returns using the dot product of simple returns and weights
        annual_return = round(np.dot(annual_returns, weights), 5) * 100
        print('\n Portfolio annual return percent:\n {} %'
              .format(str(annual_return)))
        return annual_return

# calculate simple rate of returns for securities in portfolio
simple_returns = simple_rate_of_return(port_data)

# this is to assign equal weights
weights_port_1 = np.array([0.25, 0.25, 0.25, 0.25])
# calulate portfolio annual return using the dot product of returns and weights
portfolio_1_annual_return = portfolio_annual_return_weights(simple_returns, weights_port_1)


# this is to assign equal weights
weights_port_2 = np.array([0.40, 0.30, 0.15, 0.15])
# calulate portfolio annual return using the dot product of returns and weights
portfolio_2_annual_return = portfolio_annual_return_weights(simple_returns, weights_port_2)


# this is to assign equal weights
weights_port_3 = np.array([0.25, 0.20, 0.15, 0.40])
# calulate portfolio annual return using the dot product of returns and weights
portfolio_3_annual_return = portfolio_annual_return_weights(simple_returns, weights_port_3)


#############################################################################
#                       Efficient Frontier                                  #
#############################################################################
# calculate the log returns for the securities
log_returns = np.log(port_data/port_data.shift(1))

# number of assests
num_assets = len(tickers) 

    
# intialize empty list
pfolio_returns = []
pfolio_volatilities = []

# run 1000 simulations caclulating the annualize portfolio returns
# and the volatilities for the returns
# this tries 1000 different weight combinations for the assests
for i in range (1000):
     weights = np.random.random(num_assets)
     weights /= np.sum(weights) 
     pfolio_returns.append(np.sum(weights * log_returns.mean())*250)
     pfolio_volatilities.append(np.sum(np.dot(weights.T, np.dot(log_returns.cov()*250, weights))))
    
 
# creat and store the simulations in a dataframe
portfolios = pd.DataFrame({'Return': pfolio_returns, 'Volatility': pfolio_volatilities})
# sanity check firt few rows
portfolios.head()
# sanity check last few rows
portfolios.tail()
# plot the Markowitz Efficient Frontier: Want portfolio with smallest
# expected volatility and highest expected return
portfolios.plot(x='Volatility', y ='Return', kind = 'scatter', figsize = (10, 6))
plt.title('Markowitz Efficient Frontier (AAPL, INTL, MSFT, TSLA)')
plt.xlabel('Expected Volatility')
plt.ylabel('Expected Return')
plt.savefig('Markowitz-Efficient-Frontier_pdf.pdf', 
    bbox_inches = 'tight', dpi=None, facecolor='w', edgecolor='b', 
    orientation='portrait', papertype=None, format=None, 
    transparent=True, pad_inches=0.25, frameon=None)
plt.show()
