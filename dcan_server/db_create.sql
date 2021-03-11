create table users (username text primary key not null, password_hash text not null);
create table jobs (id integer primary key AUTOINCREMENT, username text not null, job_title text not null, job_description text, job_status text not null);
create table shaders (id integer primary key AUTOINCREMENT, job_id integer not null, shader text not null);
create table datasets (id integer primary key AUTOINCREMENT, job_id integer not null, data text not null, result text, status text not null);