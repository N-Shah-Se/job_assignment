from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
import sqlite3, random, datetime
import os
from functools import wraps
import uuid
import jwt
import secret
# for encryption
from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open('secrestkey.key','wb') as filekey:
    filekey.write(key)


fernet = Fernet(key)

app = Flask(__name__)

app.config['SECRET_KEY']='004f2af45d3a4e161a7dd2d17fdae47f'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# This Code will conect and create the table in the database
def connect():
    conn = sqlite3.connect('user.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user (id VARCHAR(255) PRIMARY KEY,username Text, name TEXT, department TEXT,password Text)")
    conn.commit()
    conn.close()
# now we first look for already existing db
if os.path.isfile('user.db')==False:
    print('hello')
    connect()

# now we can check if the user token is valid or not,
def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'token' in request.headers:
           token = request.headers['token']
           print(token)
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:

            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            conn = sqlite3.connect('user.db')
            cur = conn.cursor()
            
            user_id = request.args.get('user_id')

            query= f"select * from user where id='{data['public_id']}'"
            
            cur.execute(query)
            row = cur.fetchone()
            print(row)
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(row, *args, **kwargs)
   return decorator

# user will register without authentication
@app.route('/register', methods=['POST'])
def signup_user():

    data = request.get_json() 
    hashed_password = generate_password_hash(data['password'], method='sha256')
     
    conn = sqlite3.connect('user.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO user VALUES (?,?,?,?,?)", (
    str(uuid.uuid4()),
    data['username'],
    data['name'],
    data['department'],
    hashed_password
    ))
    conn.commit()
    conn.close()

    return jsonify({
                'status': '200',
                'msg': 'User Record added Successfully'
                })
# here user will provide username and password
# if it's correct then tokens will be generated
@app.route('/login', methods=['POST'])
def user_login():

    data = request.get_json() 
    
    conn = sqlite3.connect('user.db')
    user_name = data['username']
    password = data['password']

    query= f"select * from user where username='{user_name}'"
    
    cur = conn.cursor()
    cur.execute(query)
    row = cur.fetchone()
    conn.commit()
    conn.close()
    if check_password_hash(row[4],password):
        
        jwt_token = jwt.encode({'public_id' : row[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
        
        with open('./encrypted.txt', 'wb') as file:
            
            file.write(bytes(jwt_token, 'utf-8'))

        with open('./encrypted.txt', 'rb') as file:
            
            token = file.read()

        encrypted = fernet.encrypt(token)
        
        with open('./encrypted.txt', 'wb') as file:
            
            file.write(encrypted)

        return jsonify({'encrypted_token' : jwt_token})
    else:
        return jsonify({'status' : "failed Authentication"})

@app.route("/view/", methods=['GET'])
@token_required
def view_user(current_user):
    
    conn = sqlite3.connect('user.db')
    cur = conn.cursor()
    
    user_id = request.args.get('user_id')

    query= f"select * from user where id={user_id}"
    
    
    if user_id == '':
    	query="select * from user"	
    
    cur.execute(query)
    row = cur.fetchall()
    
    user_records = []

    for record in row:
    	user_dct = {}
    	user_dct['user_id'] = record[0]
    	user_dct['username'] = record[1]
    	user_dct['name'] = record[2]

    	user_records.append(user_dct)
    conn.commit()
    conn.close()

    with open('./encrypted.txt', 'wb') as file:
            
            file.write(bytes(str(user_records), 'utf-8'))

    with open('./encrypted.txt', 'rb') as file:
        
        data = file.read()

    encrypted = fernet.encrypt(data)
    
    with open('./encrypted.txt', 'wb') as file:
        
        file.write(encrypted)

    return jsonify({
    				'status': '200',
    				"encrypted" : "Use decryption file to see the results"
            		})

@app.route("/delete/", methods=['DELETE'])
@token_required
def deleteRecord(current_user):
    
    conn = sqlite3.connect('user.db')
    cur = conn.cursor()
    user_id = request.args.get('user_id')
    if user_id == current_user[0]:
        return jsonify({
            "status":"200",
            "response":"Can't Delete Your Self"
            })
    query= f"delete from user where id = '{user_id}' "
    
    if user_id == '':
    	query=f"delete from user where not id='{current_user[0]}'"	
    
    cur.execute(query)
    conn.commit()
    conn.close()

    return jsonify({
    				'status': '200',
    				"result" :"User Record Deleted Successfully" 
            		})


@app.route("/update", methods=['PUT'])
@token_required
def updateRequest(current_user):
    
    data = request.get_json()
    
    if data['name']=='':
    	return ''

    user_id = current_user[0]
    name = data['name']
    department = data['department']
    password = hashed_password = generate_password_hash(data['password'], method='sha256')

    conn = sqlite3.connect('user.db')
    cur = conn.cursor()
    cur.execute(f"update user set name = ? , department= ? , password=? where id = ? ",(name,department,password,user_id))
    conn.commit()
    conn.close()

    return jsonify({
    				'status': '200',
	                'msg': 'User Record Updated Successfully'
            		})


if __name__=='__main__':
	app.run(host='0.0.0.0',port=5000,debug=True)











