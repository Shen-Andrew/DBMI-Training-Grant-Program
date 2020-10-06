"""Faculty functions"""
"""
Contains:
add_faculty
get_faculty_info_by_name
get_faculty_by_grant_title
generate_faculty_info
"""




#######################################
def add_faculty(faculty_member):
    """
    Faculty Contains: Name, Degree, Rank, Department, Interest, Role,
                      Predocs Training, Predocs Graduated, Predocs Continued Research,
                      Postdocs Training, Postdocs Graduated, Postdocs Continued Research

    Given a dictionary containing values for faculty
    Adds their information to the `Faculty Members` table
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


    Name = faculty_member["Name"]
    Degree = faculty_member["Degree"]
    Rank = faculty_member["Rank"]
    Department = faculty_member["Department"]
    Interest = faculty_member["Interest"]
    Role = faculty_member["Role"]


    sql_query = f"INSERT INTO `Faculty Members` \
    (`Name`, `Degree`, `Rank`, `Department`, `Interest`, `Role`) \
    VALUES \
    ( \
    '{new_id}', \
    '{Name}', \
    '{Degree}', \
    '{Rank}', \
    '{Department}', \
    '{Interest}', \
    '{Role}');"

    try:
        cursor.execute(sql_query);
        connection.commit()

    except Exception as e:
        return ("Exception : ", e)

    connection.close();
    return




#######################################
def get_faculty_info_by_name(faculty_name):
    """
    Given a Faculty Member's name, returns a dictionary containing:
    faculty_id
    dept_id
    name
    degree
    rank
    interest
    role
    """
    import pymysql
    connection = pymysql.connect(host='dbmi-sqldb.cxaqiglv703t.us-west-1.rds.amazonaws.com',
                                 user='dbmidatabase',
                                 password='dbmidatabasepassword',
                                 db='mydb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM `Faculty` where `name` = '{faculty_name}';")
    faculty_info = cursor.fetchall()[0]


    connection.close();
    return faculty_info




#######################################
def get_faculty_by_grant_title(grant_title):
    """
    Given a grant_title, returns a list of all faculty member names on the grant
    """

    import pymysql
    connection = pymysql.connect(host='dbmi-sqldb.cxaqiglv703t.us-west-1.rds.amazonaws.com',
                                 user='dbmidatabase',
                                 password='dbmidatabasepassword',
                                 db='mydb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    get_grant_id = f"SELECT grant_id FROM `Grants` where `grant_title`='{grant_title}';"
    cursor.execute(get_grant_id)
    grant_id = cursor.fetchall()[0]["grant_id"]

    get_faculty_id = f"SELECT faculty_id FROM `Trainees_has_Faculty_has_Grants` where `grant_id`={grant_id};"
    cursor.execute(get_faculty_id)
    faculty_id = cursor.fetchall()

    faculty_ids = []
    for faculty in faculty_id:
        faculty_ids.append(faculty["faculty_id"])
    faculty_ids = list(dict.fromkeys(faculty_ids))

    faculty_list = []
    for faculty_id in faculty_ids:
        get_faculty_names = f"SELECT name FROM `Faculty` where `faculty_id`={faculty_id};"
        cursor.execute(get_faculty_names)
        faculty_names = cursor.fetchall()[0]
        faculty_list.append(faculty_names["name"])

    connection.close();
    return faculty_list




#######################################
def generate_faculty_info(name):
    """
    Given a faculty members name in the form first last
    Returns a dictionary containing:
    Name
    Degree
    Rank
    Department
    Role
    Interest
    """
    name_formated = name.lower().replace(" ", ".")

    import requests

    try:
        response = requests.get(f"https://json.api.researcherprofiles.org/profiles.ucsd.edu/{name_formated}?application=ucsd_dbmi_training_grant_app&email=anshen@ucsd.edu")
        data = response.json()
    except:
        faculty_member_dict = {}
        faculty_member_dict["Name"] = name.title()
        faculty_member_dict["Degree"] = None
        faculty_member_dict["Rank"] = None
        faculty_member_dict["Department"] = None
        faculty_member_dict["Role"] = None
        faculty_member_dict["Interest"] = None
        return faculty_member_dict

    faculty_member_dict = {}

    faculty_member_dict["Name"] = name_formated.title()

    degrees = []
    for item in data["educationAndTraining"]:
        degrees.append(item["degree"])

    if degrees != []:
        degree_string = ""
        for degree in degrees:
            if degree != None:
                degree_string += degree + ", "
    else:
        degree_string = "None"

    faculty_member_dict["Degree"] = degree_string

    faculty_member_dict["Rank"] = data["titlePrimary"]

    faculty_member_dict["Department"] = data["departmentPrimary"]

    faculty_member_dict["Role"] = None

    interests_string = ""
    for item in data["keywordsFromUser"]:
        interests_string += item + ", "

    faculty_member_dict["Interest"] = interests_string.title()

    return faculty_member_dict
