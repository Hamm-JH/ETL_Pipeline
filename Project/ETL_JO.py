from Core import Core

class ETL_JO(Core):

    def __init__(self, env):
        super().__init__(env)

    def _get_data(self, date, aws_access_key_id, aws_secret_access_key, aws_s3_bucket_name, region):
        import cp2_modules.get_ as get

        return get.get_json(date, aws_access_key_id, aws_secret_access_key, aws_s3_bucket_name, region)

    def _eda(data):

        # spark eda code

        pass


