import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization


NUM_TRADING_DAYS = 252
NUM_PORTFOLIOS = 10000
stocks = ['AAPL', 'WMT', 'TSLA', 'SOFI' ]


start_date = '2021-01-01'
end_date = '2022-01-01'


def download_data():
    
    stock_data = {}
    
    for stock in stocks:
        
        ticker = yf.Ticker(stock)
        # Close : means we only care of the closing price
        stock_data[stock] = ticker.history(start=start_date, end=end_date)['Close'] 
        
        
    return pd.DataFrame(stock_data)

def show_data(data):
    data.plot(figsize=(10, 5))
    plt.show()

def calculate_return(data):
    log_return = np.log(data/data.shift(1))
    return log_return[1:]

def show_statistics(returns):
    #To calculate annual returns : 
    print(returns.mean() * NUM_TRADING_DAYS)
    print(returns.cov() * NUM_TRADING_DAYS)


def show_mean_variance(returns, weights):
    porfolio_return = np.sum(returns.mean()*weights) * NUM_TRADING_DAYS
    porfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights)))

    print("Expected portfolio mean (return): ", porfolio_return)
    print("Expected porfolio volatility (standard deviation)", porfolio_volatility)
    

def generate_portfolios(returns):
    
    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = []
    
    for _ in range(NUM_PORTFOLIOS):
        w = np.random.random(len(stocks))
        w /= np.sum(w)
        portfolio_weights.append(w)
        portfolio_means.append(np.sum(returns.mean() * w) * NUM_TRADING_DAYS)
        portfolio_risks.append(np.sqrt(np.dot(w.T, np.dot(returns.cov() * NUM_TRADING_DAYS, w))))
    
    
    return np.array(portfolio_means), np.array(portfolio_weights), np.array(portfolio_risks)

def show_portfolios(returns, volatilities):
    plt.figure(figsize=(10, 6))
    plt.scatter(volatilities, returns, c=returns/volatilities, marker='o')
    plt.grid(True)
    plt.xlabel("Expected volatility")
    plt.ylabel('Expected REturn')
    plt.colorbar(label='Sharpe Ratio')
    plt.show()

def statistics(weights, returns):
    portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights)))
    
    return np.array([portfolio_return, portfolio_volatility, portfolio_return/ portfolio_volatility])

def min_function_sharpe(weights, returns):
    return -statistics(weights, returns)[2]


# This procedure searches for the portfolio weights that maximize the Sharpe ratio, subject to constraints.
def optimize_portfolio(weights, returns):
    constraints = {'type': 'eq', 'fun' : lambda x: np.sum(x) - 1}
    
    bounds = tuple((0,1) for _ in range(len(stocks)))
    
    return optimization.minimize(fun=min_function_sharpe, x0=weights[0], args=returns, method='SLSQP', 
                          bounds=bounds, constraints=constraints)
    
def print_optimal_portfolio(optimum, returns):
    print("Optimal portfolio: ", optimum['x'].round(3))
    print("Expected return, volatility and Sharpe ratio: ", statistics(optimum['x'].round(3), returns))
    
    
def show_optimal_portfolios(opt, rets, portfolio_rets, portfolio_vols):
    plt.figure(figsize=(10, 6))
    plt.scatter(portfolio_vols, portfolio_rets, c=portfolio_rets/portfolio_vols, marker='o')
    plt.grid(True)
    plt.xlabel("Expected volatility")
    plt.ylabel('Expected REturn')
    plt.colorbar(label='Sharpe Ratio')
    opt_stats = statistics(opt['x'], rets)
    plt.plot(opt_stats[1], opt_stats[0], 'g*', markersize=20.0)
    plt.show()

        
if __name__ == '__main__':
    dataset=download_data()
    show_data(dataset)
    
    log_daily_returns = calculate_return(dataset)
    # show_statistics(log_daily_returns)
    
    
    means, pweights, risks = generate_portfolios(log_daily_returns)
    
    show_portfolios(means, risks)
    
    optimum = optimize_portfolio(pweights, log_daily_returns)
    print_optimal_portfolio(optimum, log_daily_returns)
    show_optimal_portfolios(optimum, log_daily_returns, means, risks)