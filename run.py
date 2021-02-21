from blue import app

if __name__ == "__main__":
    #app.run(debug = True)
    app.run(host="0.0.0.0", port=5000, use_reloader=False,threaded=False)
