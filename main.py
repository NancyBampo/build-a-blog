from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/newpost', methods=['POST','GET'])
def addpost():
    

    if request.method == 'POST':
        title_name = request.form['title']
        blog_name = request.form['new_blog']
        title_error = ""
        blog_error = ""
       
        if title_name == "":
            title_error = "Please fill in the title"

        if blog_name == "":
            blog_error = "Please fill in the body"
         
        if not title_error and not blog_error:
            new_blog = Blog(title_name, blog_name)
            db.session.add(new_blog)
            db.session.commit()  
            return redirect('/blog?id={}'.format(new_blog.id))
        
        else:
            return render_template('addpost.html', title_error=title_error,
            blog_error=blog_error)
    else:
        return render_template('addpost.html')
    



@app.route('/blog')
def mainblog():
    blog_id = request.args.get('id')

    if blog_id == None:
        posts = Blog.query.all()
        return render_template('blog.html', posts=posts)
    else:
        post = Blog.query.get(blog_id)
        return render_template('indi_post.html', blog=post)
    



@app.route('/')
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()


