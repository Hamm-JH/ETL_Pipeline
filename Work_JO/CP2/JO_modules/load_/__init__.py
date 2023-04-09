def load_as_csv(df, path, filename):
    """
    (test 기능) 파일이 없다면, 
    데이터를 .csv 파일로 저장
    """
    import os

    filepath = f'{path}/{filename}.csv'

    if not os.path.isfile(filepath):
        df.to_csv(filepath)