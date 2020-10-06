# Run Commands
# cd ~/github/NewerSite
# FLASK_APP=mainsite.py FLASK_DEBUG=1 flask run

from flask import Flask, render_template, request
app = Flask(__name__)


from trainee import *
from faculty import *
from grants import *
from department import *
from tables import *




# Home Page
@app.route('/')
@app.route('/Home')
def home_page():
    return render_template('home_page.html')



# Admininstrator Pages
@app.route('/admin')
def admin_main_page():
    list_of_grants = get_grant_names()
    return render_template('admin/admin_main_page.html', grants = list_of_grants)

@app.route('/admin_required_tables', methods= ['GET','POST'])
def admin_required_tables():
    global selected_grant
    selected_grant = request.form['grant_title']
    grant_info = get_grant_info_from_title(selected_grant)
    return render_template('admin/admin_required_tables.html', grant_name = selected_grant, grant_info = grant_info)

@app.route('/admin_table1')
def admin_table1():
    return render_template('admin/admin_table1.html')

@app.route('/admin_table2')
def admin_table2():
    rows = generate_table_2(selected_grant)
    return render_template('admin/admin_table2.html', data = rows)




# Department Admininstrator Pages
@app.route('/dept_admin')
def dept_admin_main_page():
    department_list = get_departments()
    return render_template('dept_admin/dept_admin_main_page.html', departments = department_list)




# PI Pages
@app.route('/pi')
def pi_main_page():
    list_of_grant_titles = get_grant_names()
    return render_template('pi/pi_main_page.html', grant_titles = list_of_grant_titles)

@app.route('/grant_faculty_list', methods= ['GET','POST'])
def pi_grant_faculty():
    global selected_grant
    selected_grant = request.form['grant_title']
    grant_info = get_grant_info_from_title(selected_grant)
    faculty_on_grant = get_faculty_by_grant_title(selected_grant)
    return render_template('pi/pi_grant_faculty.html', grant_title = selected_grant, grant_info = grant_info, faculty_list = faculty_on_grant)

@app.route('/input_form_faculty', methods= ['GET','POST'])
def pi_input_form_faculty():
    global selected_faculty
    selected_faculty = request.form['faculty']
    department_list = get_departments()
    trainee_list = get_trainees_by_faculty_name(selected_faculty)
    faculty_info = get_faculty_info_by_name(selected_faculty)
    department_name = get_department_name_from_id(faculty_info["dept_id"])
    return render_template('pi/pi_input_form_faculty.html', faculty_member = selected_faculty, departments = department_list, trainees = trainee_list, faculty_info = faculty_info, department_name = department_name)

@app.route('/input_form_new_faculty', methods= ['GET','POST'])
def pi_input_form_new_faculty():
    department_list = get_departments()
    new_member = request.form['new_member_name'].title()
    member_info = generate_faculty_info(new_member)
    return render_template('pi/pi_input_form_new_faculty.html', name = new_member, info = member_info, departments = department_list, grant_title = selected_grant)

@app.route('/add_new_faculty_to_database', methods= ['GET','POST'])
def pi_add_new_faculty_to_database():
    names = request.form['faculty_name']
    return render_template('pi/pi_add_new_faculty_to_database.html')

@app.route('/input_form_trainee', methods= ['GET','POST'])
def pi_input_form_trainee():
    return render_template('pi/pi_input_form_trainee.html', faculty_member = selected_faculty)

@app.route('/input_form_reserach_support', methods= ['GET','POST'])
def pi_input_form_reserach_support():
    return render_template('pi/pi_input_form_research_support.html', faculty_member = selected_faculty)




# Faculty Pages
@app.route('/faculty', methods= ['GET','POST'])
def faculty_input_form():
    global selected_faculty
    selected_faculty = "New Member"
    department_list = get_departments()
    trainee_list = get_trainees_by_faculty_name(selected_faculty)
    return render_template('faculty/faculty_input_form.html', faculty_member = selected_faculty, departments = department_list, trainees = trainee_list)

@app.route('/faculty_new_faculty_input_form', methods= ['GET','POST'])
def new_faculty_input_form():
    department_list = get_departments()
    new_member = request.form['new_member_name'].title()
    member_info = generate_faculty_info(new_member)
    return render_template('faculty/new_faculty_input_form.html', name = new_member, info = member_info, departments = department_list, grant_title = selected_grant)

@app.route('/faculty_add_new_faculty_to_database', methods= ['GET','POST'])
def faculty_add_new_faculty_to_database():
    names = request.form['faculty_name']
    return render_template('faculty/add_new_faculty_to_database.html')

@app.route('/faculty_input_form_trainee', methods= ['GET','POST'])
def faculty_trainee_input_form():
    return render_template('faculty/faculty_input_form_trainee.html', faculty_member = selected_faculty)

@app.route('/faculty_input_form_reserach_support', methods= ['GET','POST'])
def faculty_reserach_support_input_form():
    return render_template('/faculty/faculty_research_support_input_form.html', faculty_member = selected_faculty)




# Other Pages for testing/access
@app.route('/other')
def other_page_links():
    return render_template('other_page_links.html')


# Trainee Pages
@app.route('/Trainee_App')
def trainee_main_page():
    return render_template('trainee/trainee_main_page.html')


# Search Page for Student Publications
@app.route('/search')
def pubmed_search():
    return render_template('pubmed_search.html')
# Display Search Results
@app.route('/search/results', methods=['POST'])
def pubmed_search_results():
    text = request.form['text']
    return Search_Pubmed(text)
