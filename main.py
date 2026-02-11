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
@app.route("/create", methods=["GET", "POST"])
def create():
    myid = str(uuid.uuid1())
    
    if request.method == "GET":
         return render_template("create.html", myid=myid)

    if request.method == "POST":
        
        # Check if it's an AI automation request
        topic = request.form.get("topic")
        
        if topic:
            # --- AI AUTOMATION PATH ---
            print(f"Generating for topic: {topic}")
            
            # Create a unique ID for this folder
            rec_id = str(uuid.uuid4())
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
            os.makedirs(upload_path, exist_ok=True)
            
            # Import AI util locally to avoid circular dependency issues at top
            from ai_utils import generate_script_and_prompts
            
            # Generate Script & Prompts
            ai_data = generate_script_and_prompts(topic)
            
            if ai_data:
                script_text = ai_data.get("script", "")
                prompts = ai_data.get("image_prompts", [])
                
                # Save the script (desc.txt)
                with open(os.path.join(upload_path, "desc.txt"), "w") as f:
                    f.write(script_text)
                    
                # Save the prompts for the background worker to pick up
                with open(os.path.join(upload_path, "prompts.json"), "w") as f:
                    import json
                    json.dump(prompts, f)
                    
                print(f"AI Generation started for {rec_id}")
                
                # Pass the ID to the create page so it knows what to track
                return render_template("create.html", myid=rec_id)
            else:
                return "Failed to generate AI content. Please try again."

        else:
            # --- MANUAL UPLOAD PATH (Legacy) ---
            print(request.files.keys())
    
            rec_id = request.form.get("uuid")
            desc = request.form.get("text")
            input_files = []
            print(rec_id)
            print(desc)
    
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
            os.makedirs(upload_path, exist_ok=True)
            
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


@app.route("/status/<path:video_id>")
def check_status(video_id):
    # Check if the video file exists in static/reels
    video_path = os.path.join("static", "reels", f"{video_id}.mp4")
    if os.path.exists(video_path):
        return {"status": "done"}
    else:
        return {"status": "processing"}

@app.route("/gallery")
def gallery():
    reels=os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html", reels=reels)

if __name__ == '__main__':
    app.run(debug=True)
