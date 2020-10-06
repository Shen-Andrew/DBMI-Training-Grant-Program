"""Trainee functions"""
"""
Contains:
get_trainees_by_faculty_name
get_trainee_counts_by_faculty
get_trainee_info_by_name
Search_Pubmed
"""




#######################################
def get_trainees_by_faculty_name(faculty_name):
    """
    Given a Faculty Member's name, returns a list of all trainee names under that Faculty Member
    """
    import pymysql
    connection = pymysql.connect(host='dbmi-sqldb.cxaqiglv703t.us-west-1.rds.amazonaws.com',
                                 user='dbmidatabase',
                                 password='dbmidatabasepassword',
                                 db='mydb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    if faculty_name != "New Member":
        get_faculty_id = f"SELECT faculty_id FROM `Faculty` where `name`='{faculty_name}';"
        cursor.execute(get_faculty_id)
        faculty_id = cursor.fetchall()[0]["faculty_id"]

        get_trainee_id = f"SELECT trainee_id FROM `Trainees_has_Faculty_has_Grants` where `faculty_id`={faculty_id};"
        cursor.execute(get_trainee_id)
        trainee_id = cursor.fetchall()

        trainee_ids = []
        for trainee in trainee_id:
            trainee_ids.append(trainee["trainee_id"])
        trainee_ids = list(dict.fromkeys(trainee_ids))

        trainee_list = []
        if trainee_ids[0] != None:
            for trainee_id in trainee_ids:
                get_trainee_names = f"SELECT trainee_name FROM `Trainees` where `trainee_id`={trainee_id};"
                cursor.execute(get_trainee_names)
                trainee_names = cursor.fetchall()[0]
                trainee_list.append(trainee_names["trainee_name"])
        else:
            return []
        connection.close();
        return trainee_list
    else:
        return []




#######################################
def get_trainee_counts_by_faculty(faculty_name):
    """
    Given a Faculty Member's name, returns a dictionary containing counts for:
    Predocs_Training
    Predocs_Graduated
    Predocs_Continued_Research
    Postdocs_Training
    Postdocs_Graduated
    Postdocs_Continued_Research
    """
    import pymysql
    connection = pymysql.connect(host='dbmi-sqldb.cxaqiglv703t.us-west-1.rds.amazonaws.com',
                                 user='dbmidatabase',
                                 password='dbmidatabasepassword',
                                 db='mydb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()


    get_trainee_info_from_faculty_id = f"select * from Trainees where trainee_id in \
    (select trainee_id from Trainees_has_Faculty_has_Grants where faculty_id in \
    (SELECT faculty_id FROM `Faculty` where `name`='{faculty_name}'));"
    cursor.execute(get_trainee_info_from_faculty_id)
    trainee_info = cursor.fetchall()

    pre_current = 0
    pre_graduated = 0
    pre_continued = 0
    post_current = 0
    post_graduated = 0
    post_continued = 0

    for trainee in trainee_info:
        if trainee["trainee_type"] == "Pre":
            if trainee["current_YN"] == "Y":
                pre_current += 1
            if trainee["graduated_YN"] == "Y":
                pre_graduated += 1
            if trainee["continued_in_related_career_YN"] == "Y":
                pre_continued += 1
        if trainee["trainee_type"] == "Post":
            if trainee["current_YN"] == "Y":
                post_current += 1
            if trainee["graduated_YN"] == "Y":
                post_graduated += 1
            if trainee["continued_in_related_career_YN"] == "Y":
                post_continued += 1

    trainee_counts = {}
    trainee_counts["Predocs_Training"] = pre_current
    trainee_counts["Predocs_Graduated"] = pre_graduated
    trainee_counts["Predocs_Continued_Research"] = pre_continued
    trainee_counts["Postdocs_Training"] = post_current
    trainee_counts["Postdocs_Graduated"] =post_graduated
    trainee_counts["Postdocs_Continued_Research"] = post_continued

    connection.close();
    return trainee_counts




#######################################
def get_trainee_info_by_name(trainee_name):
    """
    Given a Trainee's name, returns a dictionary containing:
    trainee_id
    trainee_name
    trainee_type
    current_YN
    graduated_YN
    continued_in_related_career_YN
    training_start_date
    training_end_date
    """
    import pymysql
    connection = pymysql.connect(host='dbmi-sqldb.cxaqiglv703t.us-west-1.rds.amazonaws.com',
                                 user='dbmidatabase',
                                 password='dbmidatabasepassword',
                                 db='mydb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM `Trainees` where `trainee_name` = '{trainee_name}';")
    trainee_info = cursor.fetchall()[0]

    connection.close();
    return trainee_info




#######################################
def Search_Pubmed(text):
    """
    Given a name, Searches Pubmed for publications using the name
    Returns the results; if none, prints No Results Found
    """
    from pymed import PubMed
    pubmed = PubMed(tool="DBMItest", email="anshen@ucsd.edu")

    # Specifies search for author
    query = str(text) + "[Author]"
    results = pubmed.query(query, max_results=25)

    text_string = ""
    table_format = ""

    if results == None:
        return '<b>' + "No Results Found" + '</b>'

    for article in results:

        # Converts authors name from dictionary to readable format
        # Bolds the searched authors name
        authors = []
        for name in article.authors:
            individual = str(name['lastname']) + ", " + str(name['firstname'][0] + ".")
            authors.append(individual)

        author_string = ""
        if len(authors) != 1:
            for name in authors[:-1]:
                if text.split(' ', 1)[0].lower() in name.lower() \
                or text.split(' ', 1)[-1].lower() in name.lower():
                    name = '<b>' + name + '</b>'
                author_string += name + ", "
            if text.split(' ', 1)[0].lower() in authors[-1].lower() \
            or text.split(' ', 1)[-1].lower() in authors[-1].lower():
                author_string += "and " + '<b>' + str(authors[-1]) + '</b>'
            else:
                author_string += "and " + str(authors[-1])
        else:
            author_string = '<b>' + authors[0] + '</b>'

        # Combines informaiton into a printable string
        text_string += \
            "Pubmed ID: " + str(article.pubmed_id) + "<br/>" \
            "Authors: " + str(author_string) + "<br/>" \
            "Date Published: " + str(article.publication_date) + "<br/>" \
            "Title: " + str(article.title) + "<br/><br/>"

        table_format += \
            str(author_string) + ", " + \
            str(article.publication_date) + ", " + \
            str(article.title) + \
            "<br/><br/>"

    if table_format == "":
        return '<b>' + "No Results Found" + '</b>'
    return table_format
