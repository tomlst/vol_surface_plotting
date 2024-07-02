# -*- coding: utf-8 -*-
"""
Created on Fri May 10 22:57:13 2024

@author: tomls
"""

import yfinance as yf
import implied_vol_bsm as imp
import datetime 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def draw_surface(ticker, price_mode = "mid", upper_cap = 0.3, lower_floor = -0.3, r = 5.5/100, mat = 6):
    try:
        ticker = ticker
        upper_cap = upper_cap
        lower_floor = lower_floor
        r = r
        
        strikes = []
        ivs = []
        expsinDays = []
        atm_iv = []
        atm_iv_exp_in_days = []
        
        for col in range(mat):
            ticker_obj = yf.Ticker(ticker)
            S = ticker_obj.info["currentPrice"]
            expiration_dates = yf.Ticker(ticker).options
            calls = ticker_obj.option_chain(expiration_dates[col])[0]
            
            calls = calls[calls["strike"]<S * (1+upper_cap)]
            calls = calls[calls["strike"]>S * (1+lower_floor)]

            if price_mode == "mid":
                market_prices = (calls["bid"] + calls["ask"]) / 2
            elif price_mode == "bid":
                market_prices = calls["bid"]
            elif price_mode == "ask":
                market_prices = calls["ask"]
            
            for i in range(len(calls)):
                exp_date = datetime.datetime.strptime(expiration_dates[col], '%Y-%m-%d').replace(hour=16)
                #exps.append(exp_date)
                now =  datetime.datetime.now()
                T = (exp_date - now).total_seconds() / (365.25 * 24 * 3600)
                if imp.implied_volatility(market_prices.iloc[i], S, calls["strike"].iloc[i], T, r) <= 2:
                    ivs.append(imp.implied_volatility(market_prices.iloc[i], S, calls["strike"].iloc[i], T, r))
                    expsinDays += [T * 365.25]
                    strikes.append(calls["strike"].iloc[i])
            calls = calls.reset_index(drop=True)
            atm_strike_idx = abs(calls["strike"]-S).idxmin()
            atm_iv.append(imp.implied_volatility(market_prices.iloc[atm_strike_idx], S, calls["strike"].iloc[atm_strike_idx], T, r))
            atm_iv_exp_in_days.append(T * 365.25)
        
        plt.figure(dpi = 300)
        plt.plot(atm_iv_exp_in_days,atm_iv)
        plt.title(f"ATM IV for {ticker}")
        plt.show()
            
        import plotly.graph_objects as go
        
        # Create a 3D scatter plot
        fig = go.Figure(data=[go.Scatter3d(
            x=strikes,
            y=expsinDays,
            z=ivs,
            mode='markers',
            marker=dict(
                size=5,
                color=ivs,            # Set color to correspond to the z values
                colorscale='Viridis',   # Choose a colorscale
                opacity=0.8
            )
        )])
        
        
        # Update the layout of the plot
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis_title='X Axis',
                yaxis_title='Y Axis',
                zaxis_title='Z Axis'
            )
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis_title=f'Strike Price, S={S}',
                yaxis_title='Days to Expiration',
                zaxis_title='Implied Volatility'
            ),
            title=f"{ticker}"
        )
        
        
        
        
        fig.write_html(f"{ticker}.html")
        
        import webbrowser
        webbrowser.open(f"{ticker}.html")
    except KeyError as e:
        print(f"KeyError: {e}")
        print(f"{ticker} failed to process")

#next_week_earning_tickers = pd.read_csv("run_results.csv")["tickers_ticker_name"]
for i in ["DG"]:
    draw_surface(i)

'''
def get_vol_line(ticker, expiration_date, show_K=False, upper_cap=0.2, lower_floor=-0.1, r= 5.5/100):
    ticker = yf.Ticker(ticker)
    upper_cap = upper_cap
    lower_floor = lower_floor
    
    
    S = ticker.info["currentPrice"]
    
   
    
    calls = ticker.option_chain(expiration_date)[0]
    puts = ticker.option_chain(expiration_date)[1]
    
    calls = calls[calls["strike"]<S*(1+upper_cap)]
    calls = calls[calls["strike"]>S*(1+lower_floor)]
    
    mid = (calls["bid"] + calls["ask"]) / 2
    market_price = mid
    
    exp_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d')
    exp_date = exp_date.replace(hour=16)
    now =  datetime.datetime.now()
    T = (exp_date - now).total_seconds() / (365.25 * 24 * 3600)
    K = calls["strike"]
    chain_len = len(market_price)
    
    iv = []
    for i in range(chain_len):
        try:
            # Attempt to calculate the implied volatility
            iv_value = imp.implied_volatility(market_price.iloc[i], S, K.iloc[i], T, r, option_type="call")
            iv.append(iv_value)
        except:
            # If an error occurs, append 0 instead
            iv.append(0)
            
    if show_K:
        return K,iv
    else:
        return iv


ticker = "TTWO"
expiration_dates = yf.Ticker(ticker).options
num_exp_dates = len(expiration_dates)
Ks = get_vol_line(ticker, expiration_dates[0],show_K=True)[0].to_list()
num_Ks = len(Ks)
#vol_lines = pd.DataFrame(np.zeros([num_Ks,num_exp_dates]),columns=expiration_dates,index=Ks)
vol_lines = pd.DataFrame()
for exp_date in range(num_exp_dates):
    vol_lines[expiration_dates[exp_date]] = get_vol_line(ticker, expiration_dates[exp_date])
'''

