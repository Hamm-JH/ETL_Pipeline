def extract_col_1(file_path):
    """
    경로의 파일을 Task_1 에 맞게 컬럼추출
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

def merge_df_1(path):
    """
    경로 안의 모든 데이터 병합
    (2가지 형태의 DF)
    """
    import os
    import pandas as pd

    df_list1 = []

    dir_list = os.listdir(path)
    for dir in dir_list:
        dir_path = f'{path}/{dir}'
        file_list = os.listdir(dir_path)
        for file in file_list:
            file_path = f'{path}/{dir}/{file}'
            df = extract_col_1(file_path)
            if len(df.columns) == 5:
                df_list1.append(df)

    column_name_ref1 = list(df_list1[0].columns)

    for df in df_list1:
        df.columns = column_name_ref1

    df_merged1 = pd.concat(df_list1, ignore_index = True)

    return df_merged1

def drop_na(df):
    """
    결측치 처리
     : 단순 삭제
    """
    return df.dropna()

def load_as_csv(df, path, filename):
    """
    데이터를 .csv 파일로 저장
    """
    import os

    filepath = f'{path}/{filename}.csv'

    if not os.path.isfile(filepath):
        df.to_csv(filepath)

def load_to_gzip(data, path, filename):
    """
    데이터프레임(.csv)을 gzip 모듈 사용하여 압축 저장
    압축레벨 조절 가능 compresslevel(default = 5)
    """
    import os
    import gzip

    filepath = f'{path}/{filename}.gz'

    if not os.path.isfile(filepath):
        with gzip.open(filepath, 'wt') as f:
            data.to_csv(f)



PATH_DIR = 'C:/Users/wldnr/OneDrive/바탕 화면/DF/Work_JO/CP2/Batch_data'
CSV_LOAD_PATH = 'C:/Users/wldnr/OneDrive/바탕 화면/DF/Work_JO/CP2/df_csv'
GZIP_LOAD_PATH = 'C:/Users/wldnr/OneDrive/바탕 화면/DF/Work_JO/CP2/df_gzip'



df1 = merge_df_1(PATH_DIR)

df1 = drop_na(df1)

load_as_csv(df1, CSV_LOAD_PATH, '20.04.01~23.01.01')

load_to_gzip(df1, GZIP_LOAD_PATH, '20.04.01~23.01.01')










