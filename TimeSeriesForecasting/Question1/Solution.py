from datetime import date, datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import itertools
import statsmodels.api as sm



def datetime_range(start, end, delta):
    current = start
    if not isinstance(delta, timedelta):
        delta = timedelta(**delta)
    while current < end:
        yield current
        current += delta


def predictTemperature(startDate, endDate, temperature, n):

    # Temperature data is given at hourly period between startDate and endDate
    # Number of upcoming days for which prediction is to be done = n



    # Create train dataframe
    startDate = datetime.strptime(startDate, "%Y-%m-%d")#.strftime("%d-%m-%Y")
    endDate = datetime.strptime(endDate, "%Y-%m-%d") - timedelta(seconds=1) + timedelta(days=1)
    knownTimestamps =[]
    for dt in datetime_range(startDate, endDate, {'hours': 1}):
        knownTimestamps.append(dt)

    X = pd.DataFrame({'knownTimestamps': knownTimestamps, 'temperature': temperature})

    # Index the "time" column
    X = X.set_index('knownTimestamps')

    # Convert the independent data to numeric value
    y = pd.to_numeric(X['temperature'])





    # Create test datadrame
    timestamps =[]
    startD = endDate + timedelta(seconds=1)
    endD = startD - timedelta(seconds=1) + timedelta(days=int(n))
    for dt in datetime_range(startD, endD, {'hours': 1}):
        timestamps.append(dt)

    test = pd.DataFrame({'timestamps': timestamps})

    # number of hours for which prediction is to be made
    num_hours = int(n)*24



    # ARIMA Modelling
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    # Model Fit
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit()
                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue

    # The above output suggests that SARIMAX(1, 1, 0)x(0, 1, 0, 12) yields the lowest AIC value of 16.31497632
    mod = sm.tsa.statespace.SARIMAX(y,
                                    order=(1, 1, 0),
                                    seasonal_order=(0, 1, 0, 12),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()
    print(results.summary().tables[1])


    # Model Prediction
    pred = results.get_forecast(steps=num_hours)
    # Confidence Intervals
    pred_ci = pred.conf_int()
    # Prediction basis mean values
    res = pred.predicted_mean


    return res



if __name__ == "__main__":

    '''
    Input Data given in question
    '''
    filename = 'input001.txt'
    f = open(filename, "r")
    a = []
    # Iterate over each line
    for line in f:
        a.append(line)

    startDate = a[0].strip('\n')
    endDate = a[1].strip('\n')
    count = int(a[2].strip('\n'))
    temperature = []
    i = 0
    while (i < count):
        item = a[i+3].strip('\n')
        i = i + 1
        temperature.append(item)
    n = a[i+3].strip('\n')

    res = predictTemperature(startDate, endDate, temperature, n)
    print(res)
    
    f.close()  # Close file
