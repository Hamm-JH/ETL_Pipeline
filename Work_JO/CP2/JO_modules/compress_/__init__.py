def load_to_gzip(data, path, filename):
    """
    (test 기능) 파일이 없다면,
    데이터프레임(.csv)을 gzip 모듈 사용하여 압축 저장
    압축레벨 조절 가능 compresslevel(default = 5)
    """
    import os
    import gzip

    filepath = f'{path}/{filename}.gz'

    if not os.path.isfile(filepath):
        with gzip.open(filepath, 'wt') as f:
            data.to_csv(f)