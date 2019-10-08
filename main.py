from flask import Flask, render_template, request, make_response


app = Flask(__name__)


@app.route("/")
def home():
    resp = make_response(render_template("index.html"))
    resp.set_cookie('sessionID', '561')
    return resp

@app.route("/test")
def test():
    return render_template("test.html")

@app.route('/getcookie')
def getcookie():
   id = request.cookies.get('sessionID')
   return "<h1>"+ str(id) + "</h1>"

if __name__ == "__main__":
    app.run(debug=True)
