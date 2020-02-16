import psycopg2
import dbexec
from dbmeta import Meta, Table, Column

def get_meta_data(conn):
    """Populates a dbmeta.Meta object with Tables, Columns and inter-Table relationships"""
    meta = Meta()
    load_columns(conn, meta)  # Same query as exercise 1.
    constraints = load_table_constraints(conn) # constraint_name -> table mapping
    load_relationships(conn, meta, constraints)
    return meta

def load_columns(conn, meta: Meta):
    c = conn.cursor()
    # query = """select distinct table_name,column_name,case when constraint_type='PRIMARY KEY' then '*' else '' end as is_pk,data_type from information_schema.key_column_usage join information_schema.table_constraints using (table_name,constraint_name) join information_schema.columns using (table_name,column_name) order by table_name,is_pk desc,column_name;"""
    query = """with temp as (select K.table_name, K.column_name from information_schema.table_constraints as T, information_schema.key_column_usage as K where T.constraint_type = 'PRIMARY KEY' and T.constraint_name = K.constraint_name), columns as (SELECT TABLE_NAME, COLUMN_NAME, data_type FROM information_schema.COLUMNS where table_schema = 'public') select columns.table_name, columns.column_name, case when columns.column_name = temp.column_name then '*' else '' end as is_pk, columns.data_type from columns left join temp using (table_name,column_name) order by table_name,column_name;"""
    (header, rows) = dbexec.exec_query(conn, query)
    col_list = []
    prev_tbl_name = ""
    tempc =  0
    table_list = {}
    for row in rows:
        if row[0] in table_list:
            if row[2] == '*':
                table_list[row[0]].append([row[1],row[3],True])
            else:
                table_list[row[0]].append([row[1],row[3],False])
        else:
            if row[2] == '*':
                table_list[row[0]] = [[row[1],row[3],True]]
            else:
                table_list[row[0]] =  [[row[1],row[3],False]]
    for table in table_list:
        # tbl = 
        # m = Meta()
        tbl = Table(name=table)
        tbl.columns = []
        for col in table_list[table]:
            tbl.columns.append(Column(name=col[0], table=tbl, data_type=col[1], is_pk=col[2]))
        
        meta.tables[table] = tbl
        # TODO: create Table and Column objects and attach to meta. 
    c.close()

def load_table_constraints(conn):
    table_constraints = dict() # Map of constraint name -> containing table name
    c = conn.cursor()
    # query = """select A.table_name as table1,B.table_name as table2 from table_constraints as A,table_constraints as B,referential_constraints as R where A.constraint_name=R.constraint_name and B.constraint_name=R.unique_constraint_name;"""
    query = """select constraint_name, table_name from information_schema.table_constraints  where constraint_type in ('PRIMARY KEY','FOREIGN KEY') and table_schema='public';"""
    (header, rows) = dbexec.exec_query(conn, query)
    for row in rows:
        table_constraints[row[0]] = row[1]
    # # TODO: Load table_constraints table for primary and foreign keys, and record
    # # the constraint_table and the containing table name.
    

    # c.close()
    return table_constraints

def load_relationships(conn, meta, constraints):
    c = conn.cursor()

    # TODO : query referential_constraints table, which maps constraint in one table
    #      : to unique constraint in another table
    # TODO : for each row create meta.tables[from_table].refersTo += meta.tables[to_table]
    
    # query = """select A.table_name as table1,B.table_name as table2 from information_schema.table_constraints as A,information_schema.table_constraints as B,information_schema.referential_constraints as R where A.constraint_name=R.constraint_name and B.constraint_name=R.unique_constraint_name order by A.table_name,B.table_name;"""
    query = """select constraint_name,unique_constraint_name from information_schema.referential_constraints;"""
    (header, rows) = dbexec.exec_query(conn, query)
    for row in rows:
        meta.tables[constraints[row[0]]].refersTo.append(meta.tables[constraints[row[1]]])
    c.close()
    
def to_graph(meta):
    str = ""
    for tbl in meta.tables.values():
        str += "[" + tbl.name + "|"
        str += "|".join([col.name for col in tbl.columns])
        str += "]\n"
        for t in tbl.refersTo:
            str += "[%s] -> [%s]\n"%(tbl.name, t.name)
    return str

if __name__ == "__main__":
    import config
    conn = dbexec.connect()
    meta = get_meta_data(conn) # returns dbmeta 'Meta'
    conn.close()
    print(to_graph(meta))
