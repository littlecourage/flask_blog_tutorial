from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#__name__ references this file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

#class BlogPost inherits from the database Model
class BlogPost(db.Model):
  #primary key of type Integer
  id = db.Column(db.Integer, primary_key=True)
  #must put length for type String, and can't be null
  title = db.Column(db.String(100), nullable=False)
  #text doesn't have a required Length param
  content = db.Column(db.Text, nullable=False)
  #author is required, but set to default if nothing is entered
  author = db.Column(db.String, nullable=False, default="Anonymous")
  date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  #print out str when post is created
  def __repr__(self):
    return 'Blog post ' + str(self.id)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
  if request.method == 'POST'
    post_title = request.form['title']
    post_content = request.form['content']
    new_post = BlogPost(title=post_title, content=post_content, author='Christine')
    db.session.add(new_post)
  else


  return render_template('posts.html', posts=all_posts)


#if we are running this file in the command line, we run developer/debug mode
#also allows for automatic updating on server
if __name__ == "__main__":
  app.run(debug=True)