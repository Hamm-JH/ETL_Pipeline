def extract_col_1(file_path):
    """
    경로의 n번째 파일을 Task_1 에 맞게 컬럼추출
    """
    import pandas as pd
    
    data = pd.read_csv(f'{file_path}', encoding = 'cp949')
    
    column_name = list(data.columns)
    new_column_index = [i for i in range(len(column_name)) if '먼지' in column_name[i]]
    new_column_index.append(-1)
    
    if data[data.columns[-1]].notnull().sum() == 0:
        data.reset_index(inplace = True)
        data = data.iloc[:, :-2]
        data.columns = column_name
    
    data = data.iloc[:, new_column_index]
    
    return data