from flask import Flask, render_template, request, redirect, url_for, session, make_response
import pymysql
import datetime
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsRegressor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import subprocess
import speech_recognition as sr

app = Flask(__name__)

app.secret_key = 'welcome'
global uname
global original_price, predicted_price, final_price, product_name, product_id

sid = SentimentIntensityAnalyzer()
recognizer = sr.Recognizer()

@app.route('/ViewReview', methods=['GET', 'POST'])
def ViewReview():
    if request.method == 'GET':
        global uname
        font = '<font size="3" color="black">' 
        output = '<table border="1" width="100%">'
        output += '<tr><th><font size="3" color="black">Username</font></th>'
        output += '<th><font size="3" color="black">Review</font></th>'
        output += '<th><font size="3" color="black">Sentiment</font></th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'negotiate',charset='utf8')
        index = 0
        with con:
            cur = con.cursor()
            cur.execute("select * FROM reviews")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td>"
                output += "<td>"+font+str(row[2])+"</td>"                
        return render_template('ViewReview.html', msg=output)

@app.route('/ViewOrders', methods=['GET', 'POST'])
def ViewOrders():
    if request.method == 'GET':
        global uname
        font = '<font size="3" color="black">' 
        output = '<table border="1" width="100%">'
        output += '<tr><th><font size="3" color="black">Purchaser Name</font></th>'
        output += '<th><font size="3" color="black">Product ID</font></th>'
        output += '<th><font size="3" color="black">Product Name</font></th>'
        output += '<th><font size="3" color="black">Amount</font></th>'
        output += '<th><font size="3" color="black">Purchase Date</font></th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'negotiate',charset='utf8')
        index = 0
        with con:
            cur = con.cursor()
            cur.execute("select * FROM purchaseorder where username='"+uname+"'")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td>"
                output += "<td>"+font+str(row[2])+"</td>"
                output += "<td>"+font+str(row[3])+"</td>"
                output += "<td>"+font+str(row[4])+"</td>"
        return render_template('ViewOrders.html', msg=output)

@app.route('/CompleteOrder', methods=['GET', 'POST'])
def CompleteOrder():
    global uname
    global original_price, predicted_price, final_price, product_name, product_id
    if request.method == 'POST':
        if predicted_price != 0:
            now = datetime.datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            status = "Error in cinfirming order"
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'negotiate',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO purchaseorder(username,product_id,product_name,amount,transaction_date) VALUES('"+uname+"','"+product_id+"','"+product_name+"','"+str(predicted_price)+"','"+str(current_time)+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            if db_cursor.rowcount == 1:
                status = 'Your Order completed'
        else:
            status = "First negotiate price from chatbot then confirm order"
        return render_template('UserScreen.html', msg=status)
        

@app.route('/PostReviewAction', methods=['GET', 'POST'])
def PostReviewAction():
    if request.method == 'POST':
        global uname
        review = request.form['t1']
        sentiment_dict = sid.polarity_scores(review)
        compound = sentiment_dict['compound']
        result = ''
        if compound >= 0.05 : 
            result = 'Positive'
        elif compound <= - 0.05 : 
            result = 'Negative'
        else :
            result = 'Neutral'
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'negotiate',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO reviews(username,review,sentiment) VALUES('"+uname+"','"+review+"','"+result+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        status = "Error in taking review"
        if db_cursor.rowcount == 1:
            status = 'Your review accepted & sentiment predicted : '+result            
        return render_template('PostReview.html', msg=status)    
        


@app.route('/PostReview', methods=['GET', 'POST'])
def PostReview():
    return render_template('PostReview.html', msg='')


@app.route('/UserScreen', methods=['GET', 'POST'])
def UserScreen():
    global uname
    return render_template('UserScreen.html', msg="Welcome "+uname)


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', msg='')


@app.route('/Login', methods=['GET', 'POST'])
def Login():
   return render_template('Login.html', msg='')

@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    return render_template('Signup.html', msg='')

@app.route('/ChatData', methods=['GET', 'POST'])
def ChatData():
    if request.method == 'GET':
        global predicted_price
        query = request.args.get('mytext')
        query = query.strip("\n").strip()
        output = "Sorry! i am not trained for given question"
        if 'price' in query.lower():
            output = "You can get product at $:"+str(predicted_price)
        if "final" in query.lower() or "discount" in query.lower() or "my" in query.lower():
            discount = (predicted_price / 100) * 5
            predicted_price = predicted_price - discount
            output = "The final price you can get this product is $:"+str(predicted_price)
        response = make_response(output, 200)
        response.mimetype = "text/plain"
        return response

@app.route('/record', methods=['GET', 'POST'])
def record():    
    if request.method == 'POST':
        global predicted_price
        data = request.files['data'].read()
        if os.path.exists('static/audio/audio.wav'):
            os.remove('static/audio/audio.wav')
        if os.path.exists('static/audio/audio1.wav'):
            os.remove('static/audio/audio1.wav')    
        with open("static/audio/audio.wav", "wb") as fh:
            fh.write(data)
        fh.close()
        path = os.path.abspath(os.getcwd())+'/static/audio/'
        print("====================="+path)
        res = subprocess.check_output(path+'ffmpeg.exe -i '+path+'audio.wav '+path+'audio1.wav', shell=True)
        with sr.WavFile(path+'audio1.wav') as source:
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="en-IN")
        except Exception as ex:
            text = "unable to recognize"
        print(text)
        query = text.strip("\n").strip()
        output = "Sorry! i am not trained for given question"
        if 'price' in query.lower():
            output = "You can get product at $:"+str(predicted_price)
        if "final" in query.lower() or "discount" in query.lower() or "my" in query.lower():
            discount = (predicted_price / 100) * 5
            predicted_price = predicted_price - discount
            output = "The final price you can get this product is $:"+str(predicted_price)
        response = make_response("Your Query : "+query+"\nChatbot: "+output, 200)
        response.mimetype = "text/plain"
        return response

@app.route('/Chatbot', methods=['GET', 'POST'])
def Chatbot():
    if request.method == 'GET':
        global original_price, predicted_price, final_price, product_name, product_id
        product_id = request.args.get('t1') #user will select product for which he want negotiate
        types = request.args.get('t2')
        dataset = pd.read_csv("Dataset/model.csv") #read dataset
        dataset.fillna(0, inplace = True) #replace missing values in dataset with 0
        products = dataset.loc[dataset['index'] == product_id] #read all rows from dataset which is matches with user selected product
        products = products.values #convert dataframe to array
        print(products)
        original_price = products[0,5] #get original price from dataset
        product_name = products[0,2] #get product name from dataset
        X = products[:,5:6] #get original prices as X training data
        Y = products[:,6:7] #get negotiating prices as Y data
        sc = MinMaxScaler(feature_range = (0, 1)) #can be used to normalize dataset
        X = sc.fit_transform(X) #normalize the X values
        Y = sc.fit_transform(Y) #normalize the Y values
        svr_regression = SVR(C=1.0, epsilon=0.2) #create SVM object
        #training SVR with X and Y data
        svr_regression.fit(X, Y.ravel()) #trained SVM with X and Y data
        #performing prediction on test data
        predict = svr_regression.predict(X) #perform prediction to get best price
        predict = predict.reshape(predict.shape[0],1)
        predict = sc.inverse_transform(predict)
        predict = predict.ravel()
        labels = sc.inverse_transform(Y)
        labels = labels.ravel()

        knn = KNeighborsRegressor(n_neighbors=2) #here we are training with KNN
        #training KNN with X and Y data
        knn.fit(X, Y.ravel())
        #performing prediction on test data
        predict = knn.predict(X)
        predict = predict.reshape(predict.shape[0],1)
        predict = sc.inverse_transform(predict)
        predict = predict.ravel()
        labels = sc.inverse_transform(Y) #back to original values from normalization
        labels = labels.ravel()
        predicted_price = predict[0] #get best predicted price
        output = "Hi! this is Nego.<br/>Your selected Product : "+product_name+".<br/>Its Current Price : "+str(original_price)+".<br/>"
        page = 'Chatbot.html'
        if types == 'voice':
            page = 'VoiceBot.html'           
        return render_template(page, msg=output)
    


@app.route('/BrowseProducts', methods=['GET', 'POST'])
def BrowseProducts():
    if request.method == 'GET':
        font = '<font size="3" color="black">' 
        output = '<table border="1" width="100%">'
        output += '<tr><th><font size="3" color="black">Product Type</font></th>'
        output += '<th><font size="3" color="black">Product Name</font></th>'
        output += '<th><font size="3" color="black">Description</font></th>'
        output += '<th><font size="3" color="black">Product Image</font></th>'
        output += '<th><font size="3" color="black">Price</font></th>'
        output += '<th><font size="3" color="black"><font size="3" color="black">Text Negotiate with Chatbot</font></th>'
        output += '<th><font size="3" color="black"><font size="3" color="black">Voice Negotiate with Chatbot</font></th></tr>'
        dataset = pd.read_csv("Dataset/ecommerce.csv")
        dataset.fillna(0, inplace = True)
        dataset = dataset.values
        for i in range(len(dataset)):
            index = str(dataset[i,0])
            types = str(dataset[i,1])
            name = str(dataset[i,2])
            desc = str(dataset[i,3])
            price = str(dataset[i,5]) 
            output+="<tr><td>"+font+types+"</font></td>"
            output+="<td>"+font+name+"</font></td>"
            output+="<td>"+font+desc+"</font></td>"
            output+='<td><img src="static/img/'+index+'.png" width="150" height="150"></img></td>'
            output+="<td>"+font+price+"</font></td>"
            output+='<td><a href="Chatbot?t1='+index+'&t2=text">Text Based Chatbot to Negotiate</a></td>'
            output+='<td><a href="Chatbot?t1='+index+'&t2=voice">Voice Based Chatbot to Negotiate</a></td></tr>'
        return render_template('BrowseProducts.html', msg=output)


@app.route('/LoginAction', methods=['GET', 'POST'])
def LoginAction():
    global uname
    if request.method == 'POST':
        user = request.form['t1']
        password = request.form['t2']
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'negotiate',charset='utf8')
        index = 0
        with con:
            cur = con.cursor()
            cur.execute("select * FROM users")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == user and password == row[1]:
                    uname = user
                    index = 1
                    break		
        if index == 0:
            return render_template('Login.html', msg="Invalid login details")
        else:
            return render_template('UserScreen.html', msg="Welcome "+uname)       


@app.route('/SignupAction', methods=['GET', 'POST'])
def SignupAction():
    if request.method == 'POST':
        user = request.form['t1']
        password = request.form['t2']
        phone = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        gender = request.form['t6']
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'negotiate',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM users")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == user:
                    status = user+" Username already exists"
                    break
        if status == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'negotiate',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO users(username,password,contact_no,emailid,address,gender) VALUES('"+user+"','"+password+"','"+phone+"','"+email+"','"+address+"','"+gender+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            if db_cursor.rowcount == 1:
                status = 'Signup process completed'
        return render_template('Signup.html', msg=status)    
        
        


@app.route('/Logout')
def Logout():
    return render_template('index.html', msg='')



if __name__ == '__main__':
    app.run()










