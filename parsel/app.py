from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import hashlib


db = SQLAlchemy()

#Model
class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String)
    short_url = db.Column(db.String)

#Build the application
def create_app(settings_override = None):
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')

    #Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    db.init_app(app)

    #Home View
    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/', methods=['GET', 'POST'])
    def shrink():
        if request.method == 'POST':
            original_url = request.form.get('url')
            
            #Add utf-8 Encoding
            encoded_url = original_url.encode('utf-8')
            #Use the hash library to create a hash object
            hashObject = hashlib.md5(encoded_url)
            #Get the first four characters in the hashed value
            shrinkedUrl = hashObject.hexdigest()[:4]

            #Instantiate the database
            url = Url(long_url = original_url, short_url = shrinkedUrl)

            try:
                db.session.add(url)
                db.session.commit()
            except:
                flash("Sorry, link already exists, try again") 
        return render_template('index.html', shrinkedUrl=shrinkedUrl)

    #This view redirects the short url back to the original url
    @app.route('/<shrinkedUrl>')
    def redirect_url(shrinkedUrl):
        #Query the database for that particular url
        url = Url.query.filter(Url.short_url == shrinkedUrl).first()
        target = url.long_url
        if target[:4] != 'http':
            target = 'http://' + target
        
        return redirect(target)


    with app.app_context():
        db.create_all()

    return app