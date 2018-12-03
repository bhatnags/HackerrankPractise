import pandas as pd
import numpy as np
import re


# Complete the moneyFlowIndex function below.
def moneyFlowIndex(filename, n):
    data = pd.read_csv(filename)
    dataF = pd.DataFrame(data)
    col = dataF.loc[:, "High":"Close"]
    dataF['Typical Price'] = col.mean(axis=1)
    data1 = dataF[['Day', 'Typical Price']]
    pd.options.mode.chained_assignment = None
    data1['Day'] = data1.Day +1
    s2 = pd.Series([1, 0], index=['Day', 'Typical Price'])
    data1 = data1.append(s2, ignore_index=True)

    data1 = pd.merge(dataF, data1, on='Day')
    data1['Money Flow'] = data1['Typical Price_x'] * data1['Volume']
    data1['Positive Money Flow'] = np.where(data1['Typical Price_x'] > data1['Typical Price_y'], data1['Money Flow'], 0)
    data1['Negative Money Flow'] = np.where(data1['Typical Price_x'] < data1['Typical Price_y'], data1['Money Flow'], 0)
    data1['Positive Money Flow'] = np.where(data1['Day'] ==1, 0, data1['Positive Money Flow'])
    
    data1 = data1.rename(columns=lambda x: re.sub('_x','',x))
    data1 = data1.drop(columns=['Typical Price_y', 'Money Flow'])
    data1 = data1.drop_duplicates()
    
    data1['Positive Money Flow Sum'] = data1['Positive Money Flow'].rolling(min_periods=n, window=n).sum()
    data1['Negative Money Flow Sum'] = data1['Negative Money Flow'].rolling(min_periods=n, window=n).sum()
    
    data1 = data1.fillna(0)
    
    data1['Money Ratio'] = data1['Positive Money Flow Sum']/data1['Negative Money Flow Sum']
    data1['Money Flow Index'] = 100 * data1['Money Ratio']/(1+data1['Money Ratio'])
    print(list(data1))

    # df.loc[df['VALUE'].shift(-1)==1, 'TIME']
    data1.to_csv('out{0}{1}.csv'.format(n, n+1), index=False, header=True)



if __name__ == '__main__':
    print('Input File Name:')
    filename = input()
    print('Input Day:')
    n = int(input())

    moneyFlowIndex(filename, n)
