def asian_options_gbm(n):
    import yfinance as yf
    import numpy as np
    import matplotlib.pyplot as plt


    # Download historical data
    ticker = "RELIANCE.NS"  # Example: Apple stock
    display_data = yf.download(ticker, start="2020-01-01", end="2024-12-31")
    #print(display_data.head())

    data = yf.download("RELIANCE.NS", period="1y")
    prices = data['Close']
    price_array = prices.values
    #print(len(price_array))


    returns = np.log(prices / prices.shift(1)).dropna()
    #annual_volatility = returns.std() * np.sqrt(252)
    #historical_drift = returns.mean() * 252
    #print(f"Historical Drift{historical_drift}")
    #print(f"Annual Volatility{annual_volatility}")
    #formula for GBM s_t = s_0*exp((mu-sigma^2/2+sigma*z*sqrt(dt)))

    S_0 = 1411
    K = 1370
    dt = 1/252
    total_time = 19/252
    r = 0.06221
    N =19
    sigma = 0.231943
    mu = -0.06868
    S_paths = np.zeros((10000, N + 1))
    S_paths[:, 0] = S_0

    for i in range(10000):
        for  t in range(1,N+1):
            z = np.random.normal()
            S_paths[i, t] = S_paths[i, t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * z * np.sqrt(dt))

    s_avg = []
    s_new_mean = []
    for i in range(10000):
        s_avg.append(np.mean(S_paths[i]))
    for j in range(10000):
        s_new_mean.append((10000 * s_avg[j]-1411)/(10000-1))
    #calculating payoff for calls and puts
    #print(s_new_mean[:10])
    call = []
    put = []
    for i in range(10000):
        call.append(max(s_new_mean[i]-K,0))
        put.append(max(K-s_new_mean[i],0))
    call_mean = np.mean(call)
    put_mean = np.mean(put)
    discounted_call = call_mean*np.exp(-r*total_time)
    discounted_put = put_mean*np.exp(-r*total_time)
    print(f"Discounted call:{discounted_call}")
    print(f"Discounted put:{discounted_put}")
    #ploting the gbm eqn
    num_paths_to_plot = 50
    plt.figure(figsize=(10, 6))
    for i in range(num_paths_to_plot):
        plt.plot(S_paths[i], linewidth=1)

    plt.title("Sample Simulated Stock Price Paths (GBM)")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.grid(True)
    plt.show()

n = int(input("Enter the number of times to simulate: "))
for i in range(n):
    asian_options_gbm(n)

#for asian options the call is 43 and put is 6.4