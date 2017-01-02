#!/usr/bin/python

class UmbrellaAbstract(object):
    """
    Base class of the application, provides common needs of the whole suit.
    """

    def __init__(self, params):
        pass

    def connect_to_sourcedb(self):
        """
        Connects to the database where the data is going to be extracted from.
        """
        return DataSource(logger, cfg, db).database_connection()

    def connect_to_targetdb(self):
        """
        Connects to the target database cluster.
        """
        return DataSource(logger, cfg, db).database_connection()

    def extractor(self, query, target_file_name, chunksize):
        """
        Extracts data from the specified source database according to the
        specified query and writes them into csv files in chunks.
        """
        file = open(query, 'r')
        select_sql = " ".join(file.readlines())
        DataSource(logger, cfg, self.dbname).download_data_as_csv(select_sql, target_file_name, chunksize)

    def loader(self, targettable):
        """
        Fetches csv data from S3 bucket and loads them to specified
        to specified table in Redshift.
        """
        self.s3_to_rs.copy_from_s3_to_rs(self.bucket_name, targettable)

    def clean_s3_bucket(self, file_predicate):
        """
        Deletes the content of S3 bucket which starts with `file_predicate`.
        """
        self.s3manager.clean_s3_bucket(self.bucket_name, file_predicate)

    def upload_to_s3(self, filename):
        """
        Uploads the file from the disk to S3 Bucket.
        """
        self.ec2_to_S3.upload_from_ec2_to_s3(self.bucket_name, filename)


class UmbrellaMove(object):
    """
    3rd branch of Factory Pattern which is returned if truncate and
    load is necessary.
    """
    def __init__(self, params):
        pass

     def truncate_table(self):
        """
        Truncates the data of the destination table.
        """
        pass

    def create_tabe(self):
        """
        Creates the table in destination table according to
        given table definitions.
        """
        pass

    def extractor(self):
        super(ETLMove, self).extractor(self.query, self.target_file_name, self.chunksize)

    def loader(self):
        super(ETLMove, self).loader(self.targettable)


class UmbrellaSync(object):
    """
    Simply compares the primary keys of two tables and loads the diff.
    Returned by Factory if operation is `sync`.
    """
    pass


class UmbrellaUpdateInsert(object):
    """
    Checks if there is an updated column, if yes, updates in target table.
    """
    pass


class ETL(object):
    """
    Main class of the `factory pattern` to decide where to create the
    object from according to the parameter `operation.`.
    """

    @staticmethod
    def etl_runner(params):
        """
        ETL runner to kick-off the ETL process. ETL object(s) are created by this method.
        """

        if etl_params['operation'] == 'move':
            return UmbrellaMove(params)

        elif etl_params['operation'] == 'sync':
            return UmbrellaSync(params)

        elif etl_params['operation'] == 'updateorinsert':
            return UmbrellaUpdateInsert(params)
