from datetime import date, datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import itertools
import statsmodels.api as sm


def predictMissingHumidity(startDate, endDate, knownTimestamps, humidity, timestamps):

    # Humidity data is given at periodic timestamps (hourly level), these are 'knownTimestamps"
    # Humidity prediction is to be done for given timestamps 'timestamps'

    # Create train dataframe
    X = pd.DataFrame({'knownTimestamps': knownTimestamps, 'humidity': humidity})

    # Create test datadrame
    test = pd.DataFrame({'timestamps': timestamps})

    # Index the "time" column
    X = X.set_index('knownTimestamps')

    y = pd.to_numeric(X['humidity'])
    # print(y.dtypes)

    # y.plot(figsize=(15, 6))
    # plt.show()

    # ARIMA Modelling
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    # Model fit
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

    # The above output suggests that SARIMAX(1, 0, 0)x(0, 0, 0, 12) yields the lowest AIC value of -61.51893404

    mod = sm.tsa.statespace.SARIMAX(y,
                                    order=(1, 0, 0),
                                    seasonal_order=(0, 0, 0, 12),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()
    # print(results.summary().tables[1])

    # Model Prediction
    # pred = results.get_prediction()
    pred_uc = results.get_forecast(steps=5)
    pred_ci = pred_uc.conf_int()
    mean = pred_uc.predicted_mean

    return mean




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
    knownTimestamps = []
    i = 3
    count+=i
    while (i < count):
        item = a[i].strip('\n')
        i=i+1
        knownTimestamps.append(item)

    count = int(a[i].strip('\n'))
    count+=i
    humidity = []
    i=i+1
    while (i < count+1):
        item = a[i].strip('\n')
        i=i+1
        humidity.append(item)

    count = int(a[i].strip('\n'))
    count+=i
    timestamps = []
    while (i < count+1):
        item = a[i].strip('\n')
        i=i+1
        timestamps.append(item)


    res = predictMissingHumidity(startDate, endDate, knownTimestamps, humidity, timestamps)
    print(res)

    f.close()  # Close file


