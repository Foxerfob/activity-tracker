import psycopg2

def SQL_Request(DB_Settings: dict, sql: str, param: tuple = tuple()):
    conn = psycopg2.connect(
        dbname=DB_Settings["dbname"], 
        user=DB_Settings["user"], 
        password=DB_Settings["password"], 
        host=DB_Settings["host"], 
        port=DB_Settings["port"]
    )
    
    cur = conn.cursor()
    cur.execute(sql, param)
    try:
        result = cur.fetchall()
    except:
        result = None

    conn.commit()
    cur.close()
    conn.close()
    return result

def db_log(DB_Settings: dict, categoryid: int, logdescription: str, logstarttime: str, logendtime: str):
    sql = """
    INSERT INTO Logs (categoryid, logdescription, logstarttime, logendtime)
    VALUES (%s, %s, %s, %s);
    """
    SQL_Request(DB_Settings, sql, (categoryid, logdescription, logstarttime, logendtime));

def getCategories(DB_Settings: dict):
    sql = """
    SELECT * FROM categories;
    """
    return SQL_Request(DB_Settings, sql)

def getLogs(DB_Settings: dict, sqlConditions: list):
    sql = f"""
    SELECT 
        logs.logid,
        logs.logdescription,
        categories.categoryname,
        TO_CHAR(
            logs.logendtime - logs.logstarttime,
            'HH24:MI:SS'
        ) AS duration,
        logs.logstarttime,
        logs.logendtime 
        FROM logs
    JOIN 
        categories ON logs.categoryid = categories.categoryid
    {"WHERE" if len(sqlConditions) else ''}
        {' AND '.join(sqlConditions)}
    ORDER BY
        logs.logid
    ;
    """

    return SQL_Request(DB_Settings, sql)

def getSumLogs(DB_Settings: dict, sqlConditions: list):
    sql = f"""
    SELECT 
        categories.categoryname,
        TO_CHAR(
            INTERVAL '1 second' * SUM(EXTRACT(EPOCH FROM (logs.logendtime - logs.logstarttime))), 
            'HH24:MI:SS'
        ) AS total_time_formatted
    FROM logs
    JOIN 
        categories ON logs.categoryid = categories.categoryid
    {"WHERE" if len(sqlConditions) else ''}
        {' AND '.join(sqlConditions)}
    GROUP BY 
        categories.categoryname
    ;
    """

    return SQL_Request(DB_Settings, sql)
