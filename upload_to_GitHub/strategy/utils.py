# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 13:32:18 2025

@author: zipi
"""
import numpy as np

def toDictionary(df):
    KBar_dic = df.to_dict()
    #type(KBar_dic)
    #KBar_dic.keys()  ## dict_keys(['time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'product'])
    #KBar_dic['open']
    #type(KBar_dic['open'])  ## dict
    #KBar_dic['open'].values()
    #type(KBar_dic['open'].values())  ## dict_values
    KBar_open_list = list(KBar_dic['open'].values())
    KBar_dic['open']=np.array(KBar_open_list).astype(np.float64)
    #type(KBar_dic['open'])  ## numpy.ndarray
    #KBar_dic['open'].shape  ## (1596,)
    #KBar_dic['open'].size   ##  1596
    
    KBar_dic['product'] = np.repeat(df['product'][0], KBar_dic['open'].size)
    #KBar_dic['product'].size   ## 1596
    #KBar_dic['product'][0]      ## 'tsmc'
    
    KBar_time_list = list(KBar_dic['time'].values())
    KBar_time_list = [i.to_pydatetime() for i in KBar_time_list] ## Timestamp to datetime
    KBar_dic['time']=np.array(KBar_time_list)
    
    # KBar_time_list[0]        ## Timestamp('2022-07-01 09:01:00')
    # type(KBar_time_list[0])  ## pandas._libs.tslibs.timestamps.Timestamp
    #KBar_time_list[0].to_pydatetime() ## datetime.datetime(2022, 7, 1, 9, 1)
    #KBar_time_list[0].to_numpy()      ## numpy.datetime64('2022-07-01T09:01:00.000000000')
    #KBar_dic['time']=np.array(KBar_time_list)
    #KBar_dic['time'][80]   ## Timestamp('2022-09-01 23:02:00')
    
    KBar_low_list = list(KBar_dic['low'].values())
    KBar_dic['low']=np.array(KBar_low_list).astype(np.float64)
    
    KBar_high_list = list(KBar_dic['high'].values())
    KBar_dic['high']=np.array(KBar_high_list).astype(np.float64)
    
    KBar_close_list = list(KBar_dic['close'].values())
    KBar_dic['close']=np.array(KBar_close_list).astype(np.float64)
    
    KBar_volume_list = list(KBar_dic['volume'].values())
    KBar_dic['volume']=np.array(KBar_volume_list)
    
    KBar_amount_list = list(KBar_dic['amount'].values())
    KBar_dic['amount']=np.array(KBar_amount_list)

    return KBar_dic