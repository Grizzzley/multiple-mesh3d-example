import pandas as pd

file_obj = '.\\temp.csv'
temp_data = pd.read_csv(file_obj, header=None, encoding='utf-8')


def nested_temperature_list():
    ''' Nesting temperature data. '''
    final_list = []
    for i in range(len(temp_data)):
        slist = [item for item in temp_data.loc[i]]
        final_list.append(slist)
    return final_list
