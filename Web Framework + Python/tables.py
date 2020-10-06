"""Functions to generate Tables in NIH format"""

from trainee import *
from faculty import *
from grants import *
from department import *
from tables import *




def generate_table_2(grant_title):
    """
    Given a grant title, generates a dictionary for each
    row of the final table and adds each dictionary to a list.
    Returns a list of dictionaries containing the information for each row
    """
    list_of_faculty = get_faculty_by_grant_title(grant_title)

    rows = []
    for faculty_member in list_of_faculty:
        row = {}
        faculty_info = get_faculty_info_by_name(faculty_member)
        row["Name"] = faculty_info["name"]
        row["Degree"] = faculty_info["degree"]
        row["Rank"] = faculty_info["rank"]
        row["Dept"] = get_department_name_from_id(faculty_info["dept_id"])
        row["Interest"] = faculty_info["interest"]
        row["Role"] = faculty_info["role"]

        trainee_counts = get_trainee_counts_by_faculty(faculty_member)
        row["Predocs_Training"] = trainee_counts["Predocs_Training"]
        row["Predocs_Graduated"] = trainee_counts["Predocs_Graduated"]
        row["Predocs_Continued_Research"] = trainee_counts["Predocs_Continued_Research"]
        row["Postdocs_Training"] = trainee_counts["Postdocs_Training"]
        row["Postdocs_Graduated"] = trainee_counts["Postdocs_Graduated"]
        row["Postdocs_Continued_Research"] = trainee_counts["Postdocs_Continued_Research"]

        rows.append(row)
    return rows
