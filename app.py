import os
import datetime
import hashlib
import Crypto.Cipher
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from database import db_connect,user_reg,owner_reg,owner_login,upload_file,owner_viewfiles,upload_clouddata,user_request,owner_request,user_lastdownload
from database import onwer_viewdata,user_loginact,user_viewfile,user_viewfiledata,user_down,verify_user,verify_user2,user_finaldown,owner_update,user_down1
from werkzeug.utils import secure_filename
import cv2
from AES import AESCipher
from des import des
import random
import base64
import cv2
from stegano import lsb 
from RSA import encrypt,decrypt,generate
#from cloud import uploadFile,downloadFile,close
from sendmail import sendmail
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def FUN_root():
    return render_template("index.html")


@app.route("/owner")
def FUN_admin():
    return render_template("owner.html")

@app.route("/ownerlogact",methods = ['GET','POST'])
def owner_logact():
   if request.method == 'POST':
      status=owner_login(request.form['username'],request.form['password'])
      if status == True:
         session['username'] = request.form['username']
         return render_template("ownerhome.html",m1="sucess")
      else:
         return render_template("owner.html",m1="Login Failed")


@app.route("/user/")
def FUN_student():
       
    return render_template("user.html")   


@app.route("/userreg/")
def FUN_userreg():
    return render_template("userreg.html")


@app.route("/userregact", methods = ['GET','POST'])
def user_regact():
   if request.method == 'POST':
      status = user_reg(request.form['username'],request.form['password'],request.form['dob'],request.form['email'],request.form['city'],request.form['contactno'])
      if status == True:
       return render_template("user.html",m1="Success")
      else:
       return render_template("user.html",m1="Login failed")

@app.route("/userlogact",methods = ['GET','POST'])
def user_logact():
   if request.method == 'POST':
      status=user_loginact(request.form['email'],request.form['password'])
      if status == True:
         session['email'] = request.form['email']
         return render_template("userhome.html",m1="Success")
      else:
         return render_template("user.html",m1="Login Failed")


@app.route("/userhome")
def user_home():
      return render_template("userhome.html")

@app.route("/vf/")
def user_vf():
       viewfile = user_viewfile(session['email'])
       return render_template("vf.html", viewfiledata = viewfile)

@app.route("/vf1/", methods = ['GET', 'POST'])
def user_vf1():
        fname = request.args.get('filename')
        owner = request.args.get('owner')
        data = request.args.get('data')
        print(fname,owner,data,session['email'])
        check = user_viewfiledata(fname,owner,data,session['email'])
        if check == True:
         return render_template("vf.html",m1="Request_Sucess")         
        else:
         return render_template("vf.html",m1="Request_failed") 
            

@app.route("/download/")
def user_download():
      downloaddata = user_down(session['email'])
      return render_template("download.html", downloads = downloaddata)

@app.route("/downloadact/" , methods = ['GET', 'POST'])
def user_downloadact():
      fname = request.args.get('fname')
      downloaddata = user_down1(session['email'],fname)
      return render_template("downloadact.html", downloadview = downloaddata)

@app.route("/ownerreg/")
def FUN_ownerreg():
      return render_template("ownerreg.html")

@app.route("/ownerregact", methods = ['GET','POST'])
def FUN_ownerregact():
    if request.method == 'POST':
      status = owner_reg(request.form['username'],request.form['password'],request.form['dob'],request.form['email'],request.form['city'],request.form['contactno'])
      if status == True:
       return render_template("ownerhome.html",m1="Login sucess")
      else:
       return render_template("owner.html",m1="Login failed")


@app.route("/ownerhome")
def FUN_ownerhome():
    return render_template("ownerhome.html")

@app.route("/Upload", methods = ['GET','POST'])
def owner_upload():
   if request.method == 'POST':
      file = request.files['inputfile']
      check = upload_file(request.form['fname'],file,session['username'],"No","No")
      if check == True:
         return render_template("fileupload.html",m1="success")
      else:
         return render_template("fileupload.html",m1="Failed")

@app.route("/fileupload")
def FUN_fileupload():
         return render_template("fileupload.html")

@app.route("/ownerviewfiles")
def FUN_ownerviewfiles():
    viewdata = owner_viewfiles(session['username'])
    notes_table = zip([x[0] for x in viewdata],\
                          [x[1] for x in viewdata],\
                          [x[2] for x in viewdata],\
                          [x[3] for x in viewdata],\
                          [x[4] for x in viewdata])

    return render_template("ownerviewfiles.html",showdata = notes_table)

@app.route("/split/", methods = ['GET' , 'POST'])
def owner_split():
    fname = request.args.get('fname')
    owner = request.args.get('owner')
    data = request.args.get('data')
    size = len(data)
    l=len(data)
    leng=len(data)//3
    length=len(data)//2
    s1 = leng+leng  
    k = s1+leng    
    le = 1
    halfString=data[0:leng]
    second = data[leng:s1]
    third = data[s1:l]
    
   #   DES PART
    DESkey_16 = os.urandom(8)     
    d = des()
    encodedkey1 = base64.b64encode(DESkey_16)
    strkey = str(encodedkey1, 'utf-8')
    desencrypted = d.encrypt(DESkey_16,halfString,padding=True)
    print("Ciphered: %s" % desencrypted)
    print("encodedDESkey_16: %s" % strkey)
    fileDES= open("C:/Users/HP/Desktop/input/DES.txt", "w")
    fileDES.write(str(desencrypted.encode("utf-8")))
    fileDES.close()
    #uploadFile('DES.txt',"C:/Users/HP/Desktop/input/DES.txt")

    # AES PART
    AESkey_16 = os.urandom(16) 
    aescipher = AESCipher(AESkey_16)   
    encodedkey = base64.b64encode(AESkey_16)
    strkey1 = str(encodedkey, 'utf-8')
    aesencrypted = aescipher.encrypt(second)
    print('aesEncrypted: %s' % aesencrypted)
    print("encodedAESkey_16: %s" % strkey1)
    print("AESkey_16: %s" % AESkey_16)
   
    fileAES= open("C:/Users/HP/Desktop/input/AES.txt", "w")
    fileAES.write(str(aesencrypted))
    fileAES.close()
    #uploadFile('AES.txt',"C:/Users/HP/Desktop/input/AES.txt")

    #RSA ORIGHINAL
    key_pair = generate(8)
    print('Generated Key pairs')
    public_key = key_pair["public"]
    private_key = key_pair["private"]
    print(key_pair["public"])
    print(key_pair["private"])
     #Now encrypt
    ciphertext = encrypt(public_key, third)
    txt = ', '.join(map(lambda x: str(x), ciphertext))
    print ("Ciphertext is: ")
    print (txt)
    print(ciphertext)
    fileRSA= open("C:/Users/HP/Desktop/input/RSA.txt", "w")
    fileRSA.write(txt)
    fileRSA.close()
    #uploadFile('RSA.txt',"C:/Users/HP/Desktop/input/RSA.txt")
    val = ', '.join(map(lambda x: str(x), private_key))
    
    #close()
    status = upload_clouddata(data,fname.rstrip(),owner,desencrypted,strkey,aesencrypted,strkey1,str(txt),str(val))
    return render_template("ownerviewfiles.html",m1="sucess")

@app.route("/viewencfiles")
def owner_viewencfiles():
    splitdata = onwer_viewdata(session['username'])
    return render_template("viewencfiles.html",spliinfo = splitdata)

@app.route("/vuserreq")
def owner_vuserreq():
    userrequest = user_request(session['username'])
    return render_template("vuserreq.html",userreqdata = userrequest)

@app.route("/logout")
def FUN_logout():
    return render_template("index.html")

@app.route("/response", methods = ['GET','POST'])
def owner_response():
       fname1 = request.args.get('filename')
       data1 = request.args.get('data')
       owner1 = request.args.get('owner')       
       email1 = request.args.get('email')
       result = owner_request(fname1,owner1,email1)   
       rdata = result    
       status = owner_update(rdata,fname1,owner1,email1)
       if status == True:
          for skey,skey1,skey2,f1,f2,f3 in rdata:
               #sendmail(skey,skey1,skey2)
               filen= open("C:/Users/HP/Desktop/input/jointkey.txt", "w")
               filen.close()
               filen=open("C:/Users/HP/Desktop/input/jointkey.txt",'a') #text file where all 3 keys are stored
               filen.write(skey)
               filen.write(skey1)
               filen.write(skey2)
               filen.close
               stringkeys = 'fi'+skey+'se'+skey1+'co'+skey2+'th'
          with open("C:/Users/HP/Desktop/input/jointkey.txt",'r')as f:
               #stringkeys = f.readlines()
               print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
               print(stringkeys)
               msg= lsb.hide("C:/Users/HP/Desktop/input/bt.jpg",str(stringkeys)) #hide key in image
               msg.save("C:/Users/HP/Desktop/input/bt_sec.png") #save the embedded image
                            
               return redirect(url_for('owner_vuserreq'))
       else:
               return render_template("vuserreq.html",m1="false")           
           
@app.route("/verify1", methods = ['GET','POST'])
def user_verfiy():
    filename =request.form['filename']
    dkey = request.form['dkey']
    vdat=verify_user(filename,dkey)
    if vdat:
       return render_template("download2act.html",vdatavsend = vdat)
    else:
       return render_template("download.html",m1="no data in table")   

@app.route("/verify2", methods = ['GET','POST'])
def user_verfiy2():
    filename =request.form['filename']
    key = request.form['dkey']
    dat=verify_user2(filename,key)
    if dat:
       return render_template("download3act.html",datavsend = dat)
    else:
       return render_template("download.html",m1="no data in table")   

@app.route("/verify3", methods = ['GET','POST'])
def user_verfiy3():
    filename =request.form['filename']
    keys = request.form['dkey']
    dats=user_finaldown(filename,keys)
    if dats:
       for filename,owner in dats:
           fdata = user_lastdownload(filename,owner)
           if fdata:
            for skey,skey1,skey2,f1,f2,f3 in fdata:
             clear_msg = lsb.reveal("C:/Users/HP/Desktop/input/bt_sec.png") # take out keys from image
             print(clear_msg) # show the keys
             left = 'fi'
             right = 'se'
             left1= 'se'
             right1 = 'co'
             left2 = 'co'
             right2 = 'th'
                          
             key1 = clear_msg[clear_msg.index(left)+len(left):clear_msg.index(right)]
             key2 = clear_msg[clear_msg.index(left1)+len(left1):clear_msg.index(right1)]
             key3 = clear_msg[clear_msg.index(left2)+len(left2):clear_msg.index(right2)]

            #   DES PART
             decodedkey = base64.b64decode(key1) 
             descipherdec = des()           
             desdecrypted = descipherdec.decrypt(decodedkey,f1,padding=True)
             print('desdecrypted: %s' % desdecrypted)

           #   AES PART
            decodedkey1 = base64.b64decode(key2)            
            aescipherdec = AESCipher(decodedkey1)   
            aesdecrypted = aescipherdec.decrypt(f2)
            print('aesDecrypted: %s' % aesdecrypted)


           #   RSA PART
           rsaencrypteddata = list(f3.split(", "))
           print(rsaencrypteddata)
           rsapublickey = tuple(key3.split(", ")) 
           print(rsapublickey) 
           #decrypt
           rsadeciphertext = decrypt(rsapublickey, rsaencrypteddata)
           print(rsadeciphertext)          

           totaldata = desdecrypted+aesdecrypted+rsadeciphertext
           print('totaldata: %s' % totaldata) 
             
           file1 = open("C:/Users/HP/Desktop/input/myfile.txt","w") 
           file1.write(totaldata)    
           return render_template("download.html",m2="downlaod sucessfull") 
    else:
           return render_template("download.html",m2="downlaod failed") 

@app.route("/logout")
def admin_logout():
    return render_template("index.html")
if __name__ == "__main__":
   app.run(debug=True,host='127.0.0.1', port=5000)

