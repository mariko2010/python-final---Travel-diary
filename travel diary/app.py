from ext import app

if __name__ == '__main__':
    from routes import home, about, register, blogs, add_blog
    app.run(debug=True)