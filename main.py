# from flask import Flask, render_template,request,redirect,url_for
# import uuid
# import os
# from werkzeug.utils import secure_filename

# UPLOAD_FOLDER ='user_uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/create", methods=["GET","POST"])
# def create():
#     myid=uuid.uuid1()
#     if request.method=="POST":
#         print(request.files.keys())
#         rec_id=print(request.form.get("uuid"))
#         desc=print(request.form.get("text"))
#         for key,value in request.files.items():
#             print(key,value)
#             #upload file logic
#             file=request.files[key]
#             if file:
#                 filename = secure_filename(file.filename)
#                 if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], rec_id)):
#                     os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],rec_id))
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'],rec_id, filename))
#             #capture the description
#             with open(os.path.join(app.config['UPLOAD_FOLDER'],rec_id, "dec.txt","w"))as f:
#                       f.write(desc)
#     return render_template("create.html",myid=myid)

# @app.route("/gallery")
# def gallery():
#     return render_template("gallery.html")

# app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import uuid
import os
from werkzeug.utils import secure_filename
#uploading folder web , query= upload files flask
UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    myid = str(uuid.uuid1())
    if request.method == "POST":
        print(request.files.keys())

        rec_id = request.form.get("uuid")
        desc = request.form.get("text")
        input_files = []
        print(rec_id)
        print(desc)

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
        os.makedirs(upload_path, exist_ok=True)
        # Creates the directory (and any parent directories) if it doesn't already exist.

# exist_ok=True prevents it from throwing an error if the directory already exists.

# So it's a safe way to ensure that the target directory exists before saving files to it.

        for key, file in request.files.items():
            print(key, file)
             #upload file logic
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_path, filename))
                input_files.append(file.filename)
                print(file.filename)
             #capture the description
        with open(os.path.join(upload_path, "desc.txt"), "w") as f:
            f.write(desc)
        for fl in input_files:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "input.txt"), "a") as f:
                f.write(f"file '{fl}'\nduration 1\n")

    return render_template("create.html", myid=myid)

@app.route("/gallery")
def gallery():
    reels=os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html", reels=reels)

if __name__ == '__main__':
    app.run(debug=True)
