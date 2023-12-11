import pandas as pd
import numpy as np
from datetime import time, timedelta


dataset_1 = pd.read_csv('datasets/dataset-1.csv')
dataset_2 = pd.read_csv('datasets/dataset-2.csv')
dataset_3 = pd.read_csv('datasets/dataset-3.csv')

#Task 1

# Question 1
def generate_car_matrix(df):
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    np.fill_diagonal(car_matrix.values, 0)
    return car_matrix

# Question 2
def get_type_count(df):
    conditions = [df['car'] <= 15, (df['car'] > 15) & (df['car'] <= 25), df['car'] > 25]
    labels = ['low', 'medium', 'high']
    df['car_type'] = np.select(conditions, labels)
    count = df['car_type'].value_counts().to_dict()
    return dict(sorted(count.items()))

# Question 3
def get_bus_index(df):
    bus_index = dataset_1[dataset_1["bus"] > 2 * (dataset_1["bus"].mean())].index.tolist()
    sorted_index = sorted(bus_index)
    return sorted_index
    

# Question 4
def filter_routes(df):
    group_route = dataset_1.groupby("route")["truck"].mean()
    selected_routes = group_route[group_route > 7].index.tolist()
    return sorted(selected_routes)

# Question 5
def multiply_matrix(df):
    def modify_val(value):
        if value > 20:
            return value * 0.75
        else:
            return value * 1.25
    values = df.applymap(modify_val)
    return values

# Question 6: Time Check
def time_check(df):
    df['start_time'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_time'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['time_diff'] = df['end_time'] - df['start_time']
    
    incomplete_time_data = df.groupby(['id', 'id_2'])['time_diff'].agg(lambda x: x.sum() != timedelta(days=7, hours=23, minutes=59, seconds=59))
    
    return incomplete_time_data


# Save the results or perform further operations as needed

# Example usage:
# car_matrix_result = generate_car_matrix(dataset_1)
# print(car_matrix_result)
# type_count_result = get_type_count(dataset_1)
# bus_indexes_result = get_bus_indexes(dataset_1)
# selected_routes_result = filter_routes(dataset_1)
# modified_matrix_result = multiply_matrix(generate_car_matrix(dataset_1))

# incomplete_time_data_result = time_check(dataset_2)

# Please continue the script by implementing the remaining functions for Task 2.
