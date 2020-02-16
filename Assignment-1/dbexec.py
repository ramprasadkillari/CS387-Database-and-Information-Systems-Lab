import psycopg2
import config

def connect():
    #
    # TODO
    conn = psycopg2.connect(config.pg_connection_string)     # use config package for connection params

    return conn

def exec_query(conn, sql):
    """Execute sql query. Return header and rows"""
    # TODO: create cursor, get header from cursor.description, and execute query to fetch rows.
    cursor = conn.cursor()
    cursor.execute(sql)
    header = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    return (header, rows)

if __name__ == "__main__":
    from sys import argv
    import config

    query = argv[1]
    try:
        conn = connect()
        (header, rows) = exec_query(conn, query)
        print(",".join([str(i) for i in header]))
        for r in rows:
            print(",".join([str(i) for i in r]))
    except psycopg2.errors.Error as err:
        print("ERROR %%%%%%%%%%%%%%%% \n", err)
