# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 15:23:30 2023

@author: tomls
"""

import numpy as np
from scipy.optimize import fsolve
from scipy.stats import norm

def bsm_call_price(S, K, T, r, sigma):
    """Calculate Black-Scholes-Merton price for a call option."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def bsm_put_price(S, K, T, r, sigma):
    """Calculate Black-Scholes-Merton price for a call option."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return -S * norm.cdf(-d1) + K * np.exp(-r * T) * norm.cdf(-d2)


def implied_volatility(market_price, S, K, T, r, option_type='call'):
    """Calculate the implied volatility using BSM model and fsolve."""
    
    # Objective function to minimize: difference between market and theoretical prices
    def objective_function(sigma):
        if option_type == 'call':
            return bsm_call_price(S, K, T, r, sigma) - market_price
        else:  # Put option formula can be added here
            return - bsm_put_price(S, K, T, r, sigma) + market_price

    # Initial guess for volatility
    initial_guess = 0.2

    # Solving for sigma (volatility)
    implied_vol = fsolve(objective_function, initial_guess)[0]
    return implied_vol

def strangle_price(S, K, T, r, sigma):
    return bsm_call_price(S, K, T, r, sigma) +  bsm_put_price(S, K, T, r, sigma)

def new_breakeven(pre_S, K, T, r, strangle_income,post_sigma):
    cash = strangle_income
    def objective_function(post_S):
        return strangle_price(post_S, K, T, r, post_sigma) - cash
    breakeven_low = fsolve(objective_function, K*0.95)[0]
    breakeven_high = fsolve(objective_function, K*1.05)[0]
    return breakeven_low,breakeven_high
def strangle_abs_value(S,K):
    if S > K:
        return S - K
    else:
        return K - S

# Example 
'''
market_price = 1.6 # Example market price of the option
S = 91.54  # Current stock price
K = 82.00  # Strike price
T = 37/252  # Time to expiration in years
r = 0.0439  # Risk-free interest rate

iv = implied_volatility(market_price, S, K, T, r,"put")
print(f"Implied Volatility: {iv:.2%}")
'''