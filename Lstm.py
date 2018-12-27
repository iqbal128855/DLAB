import os
import time
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

class Lstm(object):
    """This class is used to implement lstm on time series power data
    """
    def __init__(self):
        print ("Initializing Lstm Class") 
        (_,y)=self.get_data()
        self.create_dataset(y)
        (self.dataX, self.dataY)=np.array(self.dataX),np.array(self.dataY)
        # reshape input 
        self.dataX = np.reshape(self.dataX, (self.dataX.shape[0], 1, self.dataX.shape[1]))
        self.build_model()
     
    def create_dataset(self,dataset, look_back=1):
	self.dataX, self.dataY = [], []
	for i in xrange(len(dataset)-look_back-1):
	    a = dataset[i:i+look_back]
	    self.dataX.append(a)
	    self.dataY.append(dataset[i + look_back])
        
	       
    def get_data(self):
        """This function is used to return daily data
        @returns mod_timestamp unix time of date time and hour
                 mod_val corresponding response values
        """
        input_dir="{0}{1}".format(os.getcwd(), "/Data")
        input_data=[f for f in os.listdir(input_dir) if ((os.path.isfile(os.path.join(input_dir,f))) and (os.stat(os.path.join(input_dir,f)).st_size > 0))]
        df=pd.read_csv(os.path.join(input_dir,input_data[0]))
        (timestamp,val)=(df["Hour_End"].values, df["COAST"].values)
        mod_timestamp,mod_val=[],[]
        err_count=0
        for i in xrange(len(timestamp)):
            try:
                mod_timestamp.append(time.mktime(time.strptime(timestamp[i], "%d/%m/%Y %H:%M")))
                mod_val.append(val[i])
            except ValueError as e:
                #TODO: fix value error
                continue
        
        return (mod_timestamp, mod_val)
    
    
    def build_model(self):
        """This function is used to build model
        """
        model=Sequential()
        model.add(LSTM(4, input_shape=(1, 1)))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(self.dataX, self.dataY, epochs=100, batch_size=1, verbose=2)

if __name__=="__main__":
    lstm=Lstm()
