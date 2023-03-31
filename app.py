from config import app, db


@app.route("/test")
def test():
    return "Hello World test!"

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
