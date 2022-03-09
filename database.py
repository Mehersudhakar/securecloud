import sqlite3
import hashlib
import datetime

user_db_file_location = "database_file/file_split.db"


def db_connect():
     _conn = sqlite3.connect(user_db_file_location)
     return _conn
      
def user_reg(username,password,email,dob,city,cno):
      _conn = sqlite3.connect(user_db_file_location)
      _c = _conn.cursor()
      _c.execute("insert into user values(?,?,?,?,?,?)", (username,password,email,dob,city,cno))
      _conn.commit()
      _conn.close()  
      return True

def user_loginact(email,password):
      _conn = sqlite3.connect(user_db_file_location)
      _c = _conn.cursor()
      _c.execute("select * from user where username='"+email+"' and password='"+password+"'")
      _conn.commit()
      _conn.close()  
      return True

def owner_reg(username,password,email,dob,city,cno):
      _conn = sqlite3.connect(user_db_file_location)
      _c = _conn.cursor()
      _c.execute("insert into owner values(?,?,?,?,?,?)", (username,password,email,dob,city,cno))
      _conn.commit()
      _conn.close()  
      return True

def owner_login(username,password):
      _conn = sqlite3.connect(user_db_file_location)
      _c = _conn.cursor()
      _c.execute("select * from owner where username='"+username+"' and password='"+password+"'")
      result = _c.fetchall()
      _conn.close()  
      return True

def upload_file(filename,file,username,pk,mk):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    current_timestamp = str(datetime.datetime.now())
    name = file.filename
    data = file.read()
    
    privatekey = "No"
    _c.execute("insert into file values(?,?,?,?,?,?,?,?)", (data,filename,current_timestamp,data.decode('utf-8'),username,"no","no","no"))
    _conn.commit()
    _conn.close()
    return True

def owner_viewfiles(username):
     _conn = sqlite3.connect(user_db_file_location)
     _c = _conn.cursor()
     _c.execute("select rowid, filename, data, CDate,owner from file where owner='"+username+"'")
     result = _c.fetchall()
     _conn.commit()
     _conn.close()
     return result

def upload_clouddata(data,fname,owner,desencrypted,DESkey_16,aesencrypted,AESkey_16,rsaencrypted,RSAkey_16):
     _conn = sqlite3.connect(user_db_file_location)
     _c = _conn.cursor()
     _c.execute("insert into cloudadata values(?,?,?,?,?,?,?,?,?)", (fname,owner,desencrypted,DESkey_16,aesencrypted,AESkey_16,rsaencrypted,RSAkey_16,data))
     _conn.commit()
     _conn.close()
     return True

def onwer_viewdata(username):
     _conn = sqlite3.connect(user_db_file_location)
     _c = _conn.cursor()
     _c.execute("select filename,f1,f2,f3 from cloudadata where owner='"+username+"'")
     result = _c.fetchall()
     _conn.commit()
     _conn.close()
     return result

def user_request(username):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    _c.execute("select filename,data,owner,email from request where owner = '"+username+"'")
    result = _c.fetchall()
    _conn.commit()
    _conn.close()
    return result

def owner_request(fname,owner,email):
      _conn = sqlite3.connect(user_db_file_location)
      _c = _conn.cursor()
      _c.execute("select skey,skey1,skey2,f1,f2,f3 from cloudadata where owner='"+owner+"' and filename='"+fname+"'")
      result = _c.fetchall()
     # owner_update(result,fname,owner,email)
      _conn.commit()
      _conn.close()
      return result

def owner_update(result,fname,owner,email):
     if result:
        for skey,skey1,skey2,f1,f2,f3 in result:  
          print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
          print(skey,skey1,skey2,f1,f2,f3 )
          _conn = sqlite3.connect(user_db_file_location)
          _c = _conn.cursor()
          _c.execute("update request set status= 'yes', s1='"+skey+"', s2='"+skey1+"', s3='"+skey2+"', p1='"+f1+"', p2='"+f2+"', p3='"+f3+"' where filename='"+fname+"'and email='"+email+"' and owner = '"+owner+"'")
          _conn.commit()
          _conn.close()
     return True 

def user_viewfile(email):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    _c.execute("select filename,data,owner from file")
    result = _c.fetchall()
    _conn.commit()
    _conn.close()
    return result


def user_viewfiledata(fname,owner,data,email):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    _c.execute("insert into request(filename, data, owner,status,email) values ('"+fname+"','"+data+"','"+owner+"','No','"+email+"')")
    _conn.commit()
    _conn.close()
    return True



def user_down(email):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    _c.execute("select filename,owner from request where email = '"+email+"' and status = 'yes'")
    result = _c.fetchall()
    _conn.commit()
    _conn.close()
    return result

def user_down1(email,fname):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    _c.execute("select filename,owner from request where email = '"+email+"' and status = 'yes' and filename = '"+fname+"'")
    result = _c.fetchall()
    _conn.commit()
    _conn.close()
    return result
def verify_user(filename,dkey):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    _c.execute("select filename,owner from cloudadata where filename='" + filename + "' and skey = '"+dkey+"'")
    result = _c.fetchall()
    _conn.commit()
    _conn.close()
    return result

def verify_user2(filename,dkey):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    _c.execute("select filename,owner from cloudadata where filename='" + filename + "' and skey1 = '"+dkey+"'")
    result = _c.fetchall()
    _conn.commit()
    _conn.close()
    return result

def user_finaldown(filename,dkey):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    _c.execute("select filename,owner from cloudadata where filename='" + filename + "' and skey2 = '"+dkey+"'")
    result = _c.fetchall()
    _conn.commit()
    _conn.close()
    return result

def user_lastdownload(filename,owner):
     _conn = sqlite3.connect(user_db_file_location)
     _c = _conn.cursor()
     _c.execute("select skey,skey1,skey2,f1,f2,f3 from cloudadata where owner='"+owner+"' and filename='"+filename+"'")
     result = _c.fetchall()
     _conn.commit()
     _conn.close()
     return result


if __name__ == "__main__":
    print(db_connect())