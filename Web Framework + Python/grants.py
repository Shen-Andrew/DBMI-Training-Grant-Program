"""Grant functions"""
"""
Contains:
add_grants
get_grants
get_grant_info_from_title
"""




#######################################
def add_grants(grant_info):
    """
    grant_info contains:
    {"grant_title", "award_number", "project_start_date", "project_end_date", "pdpi",
    "predoc_positions", "postdoc_positions", "short_term_positions"}

    Given a dictionary containing values for grants
    Adds their information to the `Grants` table
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


    grant_title = grant_info["grant_title"]
    award_number = grant_info["award_number"]
    project_start_date = grant_info["project_start_date"]
    project_end_date = grant_info["project_end_date"]
    pdpi = grant_info["pdpi"]
    predoc_positions = grant_info["predoc_positions"]
    postdoc_positions = grant_info["postdoc_positions"]
    short_term_positions = grant_info["short_term_positions"]


    sql_query = f"INSERT INTO `Grants` VALUES \
    (\
    '{grant_title}', \
    '{award_number}', \
    '{project_start_date}', \
    '{project_end_date}', \
    '{pdpi}', \
    '{predoc_positions}', \
    '{postdoc_positions}', \
    '{short_term_positions}', \
    );";

    try:
        cursor.execute(sql_query);
        connection.commit()

    except Exception as e:
        return ("Exception : ", e)

    return




#######################################
def get_grants():
    """
    Returns a list of all Grants currently in the database
    """

    import pymysql
    connection = pymysql.connect(host='dbmi-sqldb.cxaqiglv703t.us-west-1.rds.amazonaws.com',
                                 user='dbmidatabase',
                                 password='dbmidatabasepassword',
                                 db='mydb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    grant_list = []
    number_of_rows = (cursor.execute("SELECT * FROM `Grants`;"))
    row = cursor.fetchall()
    for i in range(number_of_rows):
        grant_list.append(row[i])

    connection.close();
    return grant_list




#######################################
def get_grant_info_from_title(grant_title):
    """
    Given a Grant's title, returns a dictionary containing:
    grant_id
    grant_title
    award_number
    project_start_date
    project_end_date
    pdpi
    predoc_positions
    postdoc_positions
    short_term_positions
    """
    import pymysql
    connection = pymysql.connect(host='dbmi-sqldb.cxaqiglv703t.us-west-1.rds.amazonaws.com',
                                 user='dbmidatabase',
                                 password='dbmidatabasepassword',
                                 db='mydb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    sql_query = f"SELECT * FROM `Grants` where `grant_title` = '{grant_title}';"

    cursor.execute(sql_query)
    grant_info = cursor.fetchall()


    connection.close();
    return grant_info
