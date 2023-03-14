import os
import json
import psycopg2


class Postgres():
    # static variable, best practice is to keep only a single connection and reuse it
    conn = None


    STAGING_UPDATE_METADATA = """
        UPDATE staging SET metadata=%(metadata)s WHERE bucket = %(bucket)s AND object = %(object)s
    """

    def __init__(self) -> None:
        if Postgres.conn is None:
            try:
                conn = psycopg2.connect(database=os.environ.get("POSTGRES_DB"),
                                        user=os.environ.get("POSTGRES_USER"),
                                        password=os.environ.get("POSTGRES_PASSWORD"),
                                        host=os.environ.get("POSTGRES_URL"),
                                        port=os.environ.get("POSTGRES_PORT"))
                Postgres.conn = conn
            except Exception as e:
                print(e)
                print("Database connection unsuccesfull. Bailing out.")
                exit(1)
    
    
    def update_metadata(self, bucket, object, metadata):
        cur = Postgres.conn.cursor()
        cur.execute(Postgres.STAGING_UPDATE_METADATA, {"bucket": bucket, "object": object, "metadata": json.dumps(metadata)})
        # was not succesfull
        if cur.rowcount == 0:
            return None
        Postgres.conn.commit()
        return 1


        

            