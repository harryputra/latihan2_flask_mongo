from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME, USER_COLLECTION, JURUSAN_COLLECTION, KOMPETENSI_COLLECTION

app = Flask(__name__)
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]
collection_user = db[USER_COLLECTION]
collection_jurusan = db[JURUSAN_COLLECTION]
collection_kompetensi = db[KOMPETENSI_COLLECTION]

@app.route('/')
def index():
    return "halo Semua"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['i_username']
        password = request.form['i_password']
        
        user = collection_user.find_one({
            'username': username, 
            'password': password
            })
        print ("ini data user ")
        print (user)
        if user:
            # return render_template('mahasiswa.html')
            return redirect('/mahasiswa')
        else:
            return render_template('login.html')
            
    
    return render_template('login.html')    


@app.route('/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():

    data_list_jurusan = collection_jurusan.find() 
    data_list_kompetensi = collection_kompetensi.find()
    # print(data_list_jurusan)
    if request.method == 'POST':
        nim = request.form['i_nim']
        nama = request.form['i_nama']
        alamat = request.form['i_alamat']
        jurusan = request.form['i_jurusan']
        jenis_kelamin = request.form['i_jns_kl']
        kompetensi= request.form.getlist('kompetensi')
        data = {
            'nim': nim, 
            'nama': nama, 
            'alamat': alamat,
            'jurusan': jurusan,
            'jenis_kelamin': jenis_kelamin,
            'kompetensi': kompetensi
            }
        collection.insert_one(data)
        return render_template('mahasiswa.html', data_jurusan=data_list_jurusan, data_kompetensi=data_list_kompetensi)
    return render_template('mahasiswa.html', data_jurusan=data_list_jurusan, data_kompetensi=data_list_kompetensi)
    
@app.route('/list_mahasiswa')
def get_list_mahasiswa():
    list_data_mhs = {}
    list_data_mhs = collection.find() 
    
    return render_template("list_mahasiswa.html", 
                           data_mahasiswa=list_data_mhs)
    
        
@app.route('/edit/<id>')
def edit_mahasiswa(id):
    data_list_jurusan = collection_jurusan.find()
    data_list_kompetensi = collection_kompetensi.find()
    mahasiswa = collection.find_one(
        {
            '_id': ObjectId(id)
            }
        )
    return render_template('edit_mahasiswa.html', 
                           mahasiswa=mahasiswa, 
                           list_jurusan=data_list_jurusan,
                           list_kompetensi=data_list_kompetensi)




@app.route('/update/<id>', methods=['POST'])
def update_mahasiswa(id):
    nim = request.form['i_nim']
    nama = request.form['i_nama']
    alamat = request.form['i_alamat']
    jurusan = request.form['i_jurusan']
    jenis_kelamin = request.form['i_jns_kl']
    kompetensi= request.form.getlist('kompetensi')
    data = {
            'nim': nim, 
            'nama': nama, 
            'alamat': alamat,
            'jurusan': jurusan,
            'jenis_kelamin': jenis_kelamin,
            'kompetensi': kompetensi
            }
    collection.update_one(
        {'_id': ObjectId(id)}, 
        {'$set': data}
        )
    return redirect('/list_mahasiswa')




if __name__ == '__main__':
    app.run(debug=True)
