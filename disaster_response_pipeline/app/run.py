#####################################################
#   Author: Gunasekar Jabbala                       #
#   Email: gunasekar.ai.dev@gmail.com               #
#####################################################

from flask import Flask, render_template, make_response

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    """
    Index page will be loaded first
    """
    return render_template("index.html")


@app.route("/go", methods=["POST", "GO"])
def go():
    """
    Index page will be loaded first
    """
    return render_template("go.html")


@app.errorhandler(404)
def not_found(error):
    """
    Index page will be loaded first
    """
    resp = make_response(render_template("error.html"), 404)
    return resp


def main():
    """
    Index page will be loaded first
    """
    print("Starting application server")
    app.run(host="0.0.0.0", port=3001, debug=True)


if __name__ == "__main__":
    main()
