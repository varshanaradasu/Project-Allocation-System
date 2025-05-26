from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager,create_access_token
from datetime import datetime,timedelta
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import csv
from flask import Response

project=Flask(__name__)
bcrypt=Bcrypt(project)
project.config['JWT_SECRET_KEY']="myapp123"
jwt=JWTManager(project)
CORS(project)

project.config['MYSQL_USER']="root"
project.config['MYSQL_PASSWORD']="sameera74"
project.config['MYSQL_DB']="project_allocation_system"
project.config['MYSQL_HOST']="localhost"
mysql=MySQL(project)

@project.route("/adduser", methods=["POST"])
def adduser():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']
    role = data['role']
    skills = data.get('skills')
    skill_rating = data.get('skill_rating')
    if not name or not email or not password or not role:
        return jsonify({"error": "Missing required fields"})
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cur.fetchone():
        return jsonify({"message": "User already exists"})
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    if role == "employee":
        cur.execute("INSERT INTO users (name, email, password, role, skills, skill_rating) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, email, hashed_password, role, skills, skill_rating))
    else:
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                    (name, email, hashed_password, role))
    mysql.connection.commit()
    return jsonify({"message": f"{role.capitalize()} added successfully"})

@project.route("/userlogin", methods=["POST"])
def userlogin():
    data = request.json  
    email = data['email']
    password = data['password']
    if not email or not password:
        return jsonify({"error": "Missing credentials"})

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, email, password FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    if not user:
        return jsonify({"message": "User not found"})

    user_id, email, password_hash = user
    if bcrypt.check_password_hash(password_hash, password):
        access_token = create_access_token(identity=str(user_id), expires_delta=timedelta(hours=1))
        return jsonify({
            "message": "Login success",
            "access_token": access_token,
            "user_id": user_id,
            "email": email
        })
    else:
        return jsonify({"message": "Login failed"})


@project.route("/viewemployees", methods=["GET"])
def get_all_employees():
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, name, email, skills, skill_rating FROM users WHERE role = 'employee'")
    rows = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    results = [dict(zip(col_names, row)) for row in rows]
    return jsonify(results)


@project.route("/addproject", methods=["POST"])
def addproject():
    data = request.json
    proj_title = data["proj_title"]
    proj_desc = data["proj_desc"]
    req_skills = data["req_skills"]
    proj_cap = data["proj_cap"]
    if not proj_title or not proj_cap:
        return jsonify({"error": "Title and capacity required"})
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO projects (proj_title, proj_desc, req_skills, proj_cap) VALUES (%s, %s, %s, %s)",
                (proj_title, proj_desc, req_skills, proj_cap))
    mysql.connection.commit()
    return jsonify({"message": "Project added successfully"})


@project.route("/viewprojects", methods=["GET"])
def viewprojects():
    cur = mysql.connection.cursor()
    cur.execute("SELECT proj_id, proj_title, proj_desc, req_skills, proj_cap, status FROM projects")
    projects = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    project_list = [dict(zip(columns, row)) for row in projects]
    return jsonify(project_list)


@project.route("/updateproject", methods=["PUT"])
def updateprojectput():
    data = request.json
    proj_id = data['proj_id']
    proj_title = data.get("proj_title")
    proj_desc = data.get("proj_desc")
    req_skills = data.get("req_skills")
    proj_cap = data.get("proj_cap")
    cur = mysql.connection.cursor()
    cur.execute("UPDATE projects SET proj_title=%s, proj_desc=%s, req_skills=%s, proj_cap=%s WHERE proj_id=%s", (proj_title, proj_desc, req_skills, proj_cap, proj_id))
    mysql.connection.commit()
    return jsonify({"message": "Project updated (PUT)"})


@project.route("/updateprojectpatch", methods=["PATCH"])
def updateprojectpatch():
    data = request.json
    proj_id = data['proj_id']
    updates = []
    values = []
    for key in ['proj_title', 'proj_desc', 'req_skills', 'proj_cap']:
        if key in data:
            updates.append(f"{key}=%s")
            values.append(data[key])
    values.append(proj_id)
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE projects SET {', '.join(updates)} WHERE proj_id=%s", values)
    mysql.connection.commit()
    return jsonify({"message": "Project updated (PATCH)"})

@project.route("/deleteproject", methods=["DELETE"])
def deleteproject():
    proj_id = request.json['proj_id']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM projects WHERE proj_id = %s", (proj_id,))
    mysql.connection.commit()
    return jsonify({"message": "Project deleted successfully"})

@project.route("/autoallocate", methods=["GET"])
def autoallocate():
    cur = mysql.connection.cursor()
    cur.execute("SELECT proj_id, req_skills, proj_cap FROM projects WHERE status IS NULL OR status != 'Completed'")
    projects = cur.fetchall()
    cur.execute("SELECT user_id, skills, skill_rating FROM users WHERE role = 'employee' ORDER BY skill_rating DESC")
    employees = cur.fetchall()
    allocated_employees = set()
    for proj in projects:
        proj_id, req_skills, proj_cap = proj
        required_skills = [skill.strip().lower() for skill in req_skills.split(',') if skill.strip()]
        allocated = 0
        for emp in employees:
            user_id, skills, rating = emp
            if user_id in allocated_employees:
                continue
            emp_skills = [s.strip().lower() for s in skills.split(',') if s.strip()]
            if any(skill in emp_skills for skill in required_skills):
                cur.execute("SELECT * FROM allocationn WHERE proj_id=%s AND user_id=%s", (proj_id, user_id))
                if not cur.fetchone():
                    cur.execute("INSERT INTO allocationn (proj_id, user_id) VALUES (%s, %s)", (proj_id, user_id))
                    allocated_employees.add(user_id)
                    allocated += 1
                if allocated >= proj_cap:
                    break
    mysql.connection.commit()
    return jsonify({"message": "Auto-allocation completed successfully."})


@project.route("/exportallocation", methods=["GET"])
def exportallocation():
    cur = mysql.connection.cursor()
    query = "SELECT p.proj_title AS Project,u.name AS Employee,u.email AS Email, a.allocated_at AS AllocatedAt FROM allocationn a JOIN users u ON a.user_id = u.user_id JOIN projects p ON a.proj_id = p.proj_id ORDER BY p.proj_title, a.allocated_at"
    cur.execute(query)
    rows = cur.fetchall()
    header = [desc[0] for desc in cur.description]
    def generate():
        data = [header] + list(rows)
        for row in data:
            yield ','.join(str(item) for item in row) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=allocations.csv"})


@project.route("/viewallocation", methods=["GET"])
def viewallocation():
    cur = mysql.connection.cursor()
    query = "SELECT a.allocation_id, u.name AS employee_name, p.proj_title AS project_name, a.allocated_at FROM allocationn a JOIN users u ON a.user_id = u.user_id JOIN projects p ON a.proj_id = p.proj_id ORDER BY p.proj_title, a.allocated_at"
    cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    result = [dict(zip(columns, row)) for row in rows]
    return jsonify(result)

@project.route('/getallocation/<int:user_id>',methods=["GET"])
def get_allocation(user_id):
    cur = mysql.connection.cursor()
    cur.execute(" SELECT p.proj_id, p.proj_title FROM allocationn a JOIN projects p ON a.proj_id = p.proj_id WHERE a.user_id = %s LIMIT 1", (user_id,))
    result = cur.fetchone()
    if result:
        return jsonify({
            "proj_id": result[0],
            "project_title": result[1]
        })
    else:
        return jsonify({"message": "No allocation found"}),

@project.route('/updatestatus', methods=['POST'])
def update_status():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(" INSERT INTO emp_status (user_id, proj_id, status)  VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE status=%s, updated_at=CURRENT_TIMESTAMP", (data['user_id'], data['proj_id'], data['status'], data['status']))
    mysql.connection.commit()
    return jsonify({"message": "Status updated successfully"})

@project.route("/viewstatuses", methods=["GET"])
def view_statuses():
    cur = mysql.connection.cursor()
    cur.execute("SELECT s.id, u.name AS employee_name, p.proj_title AS project_title, s.status, s.updated_at FROM emp_status s JOIN users u ON s.user_id = u.user_id  JOIN projects p ON s.proj_id = p.proj_id ORDER BY s.updated_at DESC")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    result = [dict(zip(columns, row)) for row in rows]
    return jsonify(result)

if __name__=="__main__":
    project.run(debug=True)
