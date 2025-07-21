from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'another_secret_key_for_blog'

blog_posts = [
    {"id": 1, "title": "Getting Started with Flask", "content": "Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.", "author": "Admin", "date": "2023-01-15"},
    {"id": 2, "title": "Understanding Jinja2 Templating", "content": "Jinja2 is a modern and designer-friendly templating language for Python, modelled after Django’s templates. It is fast, widely used, and provides flexible control structures.", "author": "Admin", "date": "2023-02-01"},
    {"id": 3, "title": "Building RESTful APIs with Flask", "content": "Flask can be effectively used to build powerful RESTful APIs. With extensions like Flask-RESTful, it becomes even easier to define resources and handle HTTP methods.", "author": "Admin", "date": "2023-03-10"},
]

@app.route('/')
def blog_home():
    query = request.args.get('q')
    if query:
        filtered_posts = [
            post for post in blog_posts 
            if query.lower() in post['title'].lower() or query.lower() in post['content'].lower()
        ]
    else:
        filtered_posts = blog_posts
    return render_template('blog_home.html', posts=filtered_posts, query=query)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = next((p for p in blog_posts if p['id'] == post_id), None)
    if post:
        return render_template('post_detail.html', post=post)
    flash('Post not found!', 'danger')
    return redirect(url_for('blog_home'))

@app.route('/admin/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form.get('author', 'Anonymous')
        
        new_id = max([p['id'] for p in blog_posts]) + 1 if blog_posts else 1
        
        new_post = {
            "id": new_id,
            "title": title,
            "content": content,
            "author": author,
            "date": "2023-XX-XX" # Simplified date
        }
        blog_posts.append(new_post)
        flash('New post added successfully!', 'success')
        return redirect(url_for('blog_home'))
    return render_template('add_post.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)