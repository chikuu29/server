import pandas as pd

import os
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up one directory to reach the project root
project_dir = os.path.dirname(current_dir)
# project_dir = os.path.dirname(os.path.abspath(__file__)) 

def get_column_data(csv_file, column_name):
    try:
        # df = pd.read_csv('../csv/'+ csv_file) 
        df=os.path.join(project_dir, 'csv_files',csv_file)
        if column_name in df.columns:
            return df[column_name].tolist()
        else:
            return []
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return []

def find_document(csv_file, key, value):
    try:
        print(f"Find",csv_file)
        # df = pd.read_csv('../csv/' + csv_file)
        path=os.path.join(project_dir, 'csv_files',csv_file)
        print("path",path)
        df = pd.read_csv(path)
        print(df)
        filtered_df = df[df[key] == value]
        return filtered_df
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return []
# Example usage
# csv_file = 'job.csv'
# key = 'job_id'
# value = '38d4f0c7-c402-4a45-ac9a-423cac83a130a'
# user_data = find_document(csv_file, key, value)
# # print(user_data)

# Example usage
# csv_file = 'job.csv'
# column_name = 'job_id'
# data = get_column_data(csv_file, column_name)


# print(data)
