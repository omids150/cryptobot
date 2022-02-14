from sklearn.preprocessing import MinMaxScaler
import numpy as np

def scaleMinMax(a):
    # use min max scaler to scale data into compareble prices 
    scaler = MinMaxScaler()

    price_array = np.array(a).reshape(-1,1)

    scaled_price = scaler.fit_transform(price_array)
    scaled_price = [float(i) for i in scaled_price] #-> problem 

    return scaled_price