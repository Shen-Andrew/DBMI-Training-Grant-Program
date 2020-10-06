"""Department functions"""
"""
Contains:
add_department
get_departments
get_department_name_from_id
"""




#######################################
def add_department(dept_name, type):
    """
    Given a department name
    Adds adds the department to the database departments table
    Does not return anything
    """

    import pymysql
    connection = pymysql.connect(host='dbmi-sqldb.cxaqiglv703t.us-west-1.rds.amazonaws.com',
                                 user='dbmidatabase',
                                 password='dbmidatabasepassword',
                                 db='mydb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    if type == "predoc":
        database_table = "Predoc_Departments"
    elif type == "postdoc":
        database_table = "Postdoc_Departments"

    get_current_max_dept_id = f"SELECT MAX(idDept) AS last_dept_id FROM `{database_table}`;"
    cursor.execute(get_current_max_dept_id)
    current_max_dept_id = cursor.fetchall()

    if lastid[0]['last_dept_id']:
        new_dept_id = lastid[0]['last_dept_id'] + 1
    else:
        new_dept_id = 1

    name = str(dept_name)
    sql_query = f"INSERT INTO `{database_table}` \
    (`idDept`, `Participating Department`)\
    VALUES ('{dept_id}', '{name}');";

    try:
        cursor.execute(sql_query);
        connection.commit()

    except Exception as e:
        print("Exception : ", e);

    connection.close();
    return




#######################################
def get_departments():
    """
    Returns a list of all the departments currently in the database
    """
    import pymysql
    connection = pymysql.connect(host='dbmi-sqldb.cxaqiglv703t.us-west-1.rds.amazonaws.com',
                                 user='dbmidatabase',
                                 password='dbmidatabasepassword',
                                 db='mydb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    get_departments = f"SELECT * FROM `Departments`;"
    cursor.execute(get_departments)
    departments = cursor.fetchall()

    department_list = []
    for dept in departments:
        department_list.append(dept["department_name"])

    connection.close();
    return department_list




#######################################
def get_department_name_from_id(id):
    """
    Returns the name of a department given an dept_id
    """
    import pymysql
    connection = pymysql.connect(host='dbmi-sqldb.cxaqiglv703t.us-west-1.rds.amazonaws.com',
                                 user='dbmidatabase',
                                 password='dbmidatabasepassword',
                                 db='mydb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    get_department_name = f"select department_name from `Departments` where dept_id = {id};"
    cursor.execute(get_department_name)
    department_name = cursor.fetchall()[0]['department_name']

    connection.close();
    return department_name
