create database project_allocation_system;
use project_allocation_system;
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY ,
    name text,
    email text,
    password text,
    role ENUM('admin', 'employee') NOT NULL,
    skills text,
    skill_rating INT
);

CREATE TABLE projects (
    proj_id SERIAL PRIMARY KEY,
    proj_title text,
    proj_desc text,
    req_skills text,
    proj_cap INT,
    status VARCHAR(50) DEFAULT 'Not Started'
);

CREATE TABLE allocationn (
    allocation_id SERIAL PRIMARY KEY,
    user_id INT,
    proj_id INT,
    allocated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE emp_status (
    id SERIAL PRIMARY KEY,
    user_id INT,
    proj_id INT,
    status VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from users;
select * from projects;
select * from allocationn;
select * from emp_status;
