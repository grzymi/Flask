
#!/usr/bin/env python
#https://stackoverflow.com/questions/34057595/allow-2-decimal-places-in-input-type-number/34057860
#http://www.pointwise.com/yplus/
#https://stackoverflow.com/questions/45149420/pass-variable-from-python-flask-to-html-in-render-template

from flask import Flask, request, render_template
from math import sqrt
from y_plus import y_plus

# create app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # show html form
        return render_template('index.html')
    elif request.method == 'POST':
        # take values from user
        
        uref = float(request.form.get('uref'))
        rho = float(request.form.get('rho'))
        mu = float(request.form.get('mu'))
        lenght = float(request.form.get('lenght'))
        Y = float(request.form.get('y+'))
        #do calculations in external function
        result = y_plus(uref, rho, mu, lenght, Y) #assign returned values
        Rex, distance = [result[i] for i in [0,1]] #assign values from position
        if Rex > 10000:
            Rex = round(Rex, 0)
        else:
            Rex = round(Rex, 2)
        return render_template ('result.html', Rex=Rex, distance=distance)


# run app
if __name__ == '__main__':
    app.run(host='192.168.0.188', port=5005, debug=True)
    #app.run(debug=True)