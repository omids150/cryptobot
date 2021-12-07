import lagtest as lg 

show_plots= True # render or dont render plots

time = 30 #how many days showld the history data go back -> only up to one 90 days possile
lag = 300 # till up to which lag do you want to compare the data 
no_splits = 100 # number of splits for window time lagges corrolation

#tezos hoch 
rand_coin_name = "tezos" #name of rand coin to get 

if __name__=="__main__":    #get bitcoin and etherium data 
    main_coin_dict = lg.get_main_coins(time=time)
    btc_df = main_coin_dict["bitcoin"]
    eth_df = main_coin_dict["ethereum"]

    #get coin to compare 
    rand_coin_df = lg.get_coin_by_name(rand_coin_name,time=time)

    btc_df, rand_coin_df = lg.clean_data(btc_df,rand_coin_df)

    # plot time series
    lg.plot_chart(btc_df,"bitcoin",rand_coin_df,rand_coin_name)

    # # detect logs 
    peak_sync,sorted_res,res = lg.detect_leg_corr(btc_df["scaled_price"],rand_coin_df["scaled_price"],lag=lag)


    # plot lag plot 
    lg.lag_plot(res,peak_snyc = peak_sync)

    # lg.windowed_time_lagged_cross_correlation(btc_df["scaled_price"],rand_coin_df["scaled_price"],lag=lag,no_splits=no_splits)

    print(peak_sync,sorted_res,res)