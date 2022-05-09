from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
from database import basedados as db
import base64

app = Flask(__name__, template_folder="templates")
app.secret_key = "a0Cbd5c2BY5HnEE4Q3FVR6bF9rWWHXQ9"

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/")
def hello_world():
    return render_template("public/index.html")

@app.route("/release/delete/<int:idRelease>/<int:idEntregavel>", methods=['POST'])
def release_delete(idRelease, idEntregavel):

    db.deleteEntregavel(idEntregavel)
    return redirect(url_for("release_view", id=idRelease))

@app.route("/release/<int:id>", methods=['GET'])
def release_view(id):
    
    release, entregas = db.getRelease(id)
    
    for entrega in entregas:
        if entrega.image01: entrega.image01 = base64.b64encode(entrega.image01).decode('ascii')
        if entrega.image02: entrega.image02 = base64.b64encode(entrega.image02).decode('ascii')

    return render_template("admin/release.html", release=release, entregas=entregas)


@app.route("/usuarios", methods=['GET'])
def usuarios_view():
    
    users = db.getUsuarios()
    return render_template("admin/usuarios.html", userList=users)


@app.route("/upload", methods=['GET'])
def upload_view():
    return render_template("public/upload.html")

@app.route('/upload', methods=['POST'])
def upload_file():

    success = False

    file01 = request.files["file01"]
    file02 = request.files["file02"]

    db.ReleaseDetalhe()
    releaseDet = db.ReleaseDetalhe()
    releaseDet.titulo = request.form["txtTitulo"]
    releaseDet.area = request.form["dropdownArea"]
    releaseDet.time = request.form["dropdownTime"]
    releaseDet.descricao = request.form["txtDescricao"]
    releaseDet.releaase_id = int(request.form["dropdownRelease"])
    if file01 and allowed_file(file01.filename): 
        
        releaseDet.image01 = file01.read()
        flash(f"arquivo: [{file01.filename}] carregado com successo", "success")

    if file02 and allowed_file(file02.filename): 

        releaseDet.image02 = file02.read()    
        flash(f"arquivo: [{file02.filename}] carregado com successo", "success")

    session = db.getSession()
    session.add(releaseDet)
    session.commit()
    session.close()


    #if file01.filename != '': file01.save("upload/" + file01.filename)
    #if file02.filename != '': file02.save("upload/" + file02.filename)
    return redirect(url_for("upload_view"))


# function to check file extension
def allowed_file(filename):
        
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(file):

    botoSession = boto3.Session(aws_access_key_id='', aws_secret_access_key='')
    s3 = botoSession.resource('s3')
    bucket = s3.Bucket('rvbrandaoreleasenotes')
    bucket.put_object(Key="1/" + file.filename, Body=file)

    return True

if __name__=="__main__":
    app.run(debug=True)