def merge_df_1(path):
    """
    경로 안의 모든 데이터 병합
    (2가지 형태의 DF)
    """
    import os
    import pandas as pd
    from JO_modules import extract_

    df_list1 = []
    df_list2 = []

    dir_list = os.listdir(path)
    for dir in dir_list:
        dir_path = f'{path}/{dir}'
        file_list = os.listdir(dir_path)
        for file in file_list:
            file_path = f'{path}/{dir}/{file}'
            df = extract_.extract_col_1(file_path)
            if len(df.columns) == 5:
                df_list1.append(df)
            else:
                df_list2.append(df)

    column_name_ref1 = list(df_list1[0].columns)
    column_name_ref2 = list(df_list2[0].columns)

    for df in df_list1:
        df.columns = column_name_ref1

    for df in df_list2:
        df.columns = column_name_ref2

    df_merged1 = pd.concat(df_list1, ignore_index = True)
    df_merged2 = pd.concat(df_list2, ignore_index = True)

    return df_merged1, df_merged2