from flask import Flask, render_template, request, redirect
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
  if request.method == 'POST':
    post_title = request.form['title']
    post_content = request.form['content']
    post_author = request.form["author"]
    new_post = BlogPost(title=post_title, content=post_content, author=post_author)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/posts')
  else:
    all_posts = BlogPost.query.order_by(BlogPost.date_created).all()
    return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
  post = BlogPost.query.get_or_404(id)
  db.session.delete(post)
  db.session.commit()
  return redirect('/posts')

@app.route('/posts/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  post = BlogPost.query.get_or_404(id)
  if request.method == 'POST':
    post.title = request.form['title']
    post.content = request.form['content']
    post.author = request.form["author"]
    db.session.commit()
    return redirect('/posts')
  else:
    return render_template('update.html', post=post)

#if we are running this file in the command line, we run developer/debug mode
#also allows for automatic updating on server
if __name__ == "__main__":
  app.run(debug=True)