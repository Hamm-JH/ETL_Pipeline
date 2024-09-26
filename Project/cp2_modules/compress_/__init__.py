def compress(data):
    import gzip
    import json

    compressed_data = gzip.compress(json.dumps(data, ensure_ascii=False, indent=4).encode('utf-8'))

    return compressed_data