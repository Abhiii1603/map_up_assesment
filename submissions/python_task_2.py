import pandas as pd

dataset_1 = pd.read_csv('datasets/dataset-1.csv')
dataset_2 = pd.read_csv('datasets/dataset-2.csv')
dataset_3 = pd.read_csv('datasets/dataset-3.csv')

def calculate_distance_matrix(dataset_3):
    # Load the dataset
    df = dataset_3


    num_rows = len(df)
    distance_matrix = pd.DataFrame(index=df['id'], columns=df['id'])

    for i in range(num_rows):
        for j in range(i, num_rows):
            if i == j:
                distance_matrix.iloc[i, j] = 0
            else:
                distance_matrix.iloc[i, j] = distance_matrix.iloc[j, i] = df.iloc[i, j]

    for i in range(num_rows):
        for j in range(i + 1, num_rows):
            for k in range(j + 1, num_rows):
                if pd.notna(distance_matrix.iloc[i, j]) and pd.notna(distance_matrix.iloc[j, k]):
                    distance_matrix.iloc[i, k] = distance_matrix.iloc[k, i] = distance_matrix.iloc[i, j] + distance_matrix.iloc[j, k]

    return distance_matrix

ans1 = calculate_distance_matrix(dataset_3)
print(ans1)




def unroll_distance_matrix(distance_matrix):
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    for i in range(len(distance_matrix.index)):
        for j in range(len(distance_matrix.columns)):
            if i != j:
                unrolled_df = unrolled_df.append({
                    'id_start': distance_matrix.index[i],
                    'id_end': distance_matrix.columns[j],
                    'distance': distance_matrix.iloc[i, j]
                }, ignore_index=True)

    return unrolled_df

unrolled_df = unroll_distance_matrix(ans1)
print(unrolled_df)


def find_ids_within_ten_percentage_threshold(unrolled_df, reference_id):
    reference_data = unrolled_df[unrolled_df['id_start'] == reference_id]

    average_distance = reference_data['distance'].mean()

    within_threshold_ids = reference_data[
        (reference_data['distance'] >= 0.9 * average_distance) &
        (reference_data['distance'] <= 1.1 * average_distance)
    ]['id_end'].tolist()

    within_threshold_ids.sort()

    return within_threshold_ids


reference_id = 1001400
result = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id)
print(result)


def calculate_toll_rate(input_df):
    result_df = input_df.copy()

    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    for vehicle_type, rate in rate_coefficients.items():
        result_df[vehicle_type] = result_df['distance'] * rate

    return result_df

toll_rate_df = calculate_toll_rate(unrolled_df)
print(toll_rate_df)


from datetime import datetime, time, timedelta

def calculate_time_based_toll_rates(input_df):
    result_df = input_df.copy()

    # Define time ranges and discount factors
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)),
                           (time(10, 0, 0), time(18, 0, 0)),
                           (time(18, 0, 0), time(23, 59, 59))]
    weekend_time_ranges = [(time(0, 0, 0), time(23, 59, 59))]
    
    weekday_discount_factors = [0.8, 1.2, 0.8]
    weekend_discount_factor = 0.7

    for start_time, end_time in weekday_time_ranges:
        mask = (result_df['start_time'] >= start_time) & (result_df['end_time'] <= end_time) & (result_df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']))
        result_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekday_discount_factors[weekday_time_ranges.index((start_time, end_time))]

    for start_time, end_time in weekend_time_ranges:
        mask = (result_df['start_time'] >= start_time) & (result_df['end_time'] <= end_time) & (result_df['start_day'].isin(['Saturday', 'Sunday']))
        result_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekend_discount_factor

    return result_df


time_based_toll_rates_df = calculate_time_based_toll_rates(toll_rate_df)
print(time_based_toll_rates_df)


