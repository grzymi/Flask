
#!/usr/bin/env python
#https://stackoverflow.com/questions/34057595/allow-2-decimal-places-in-input-type-number/34057860
#http://www.pointwise.com/yplus/
#https://stackoverflow.com/questions/45149420/pass-variable-from-python-flask-to-html-in-render-template

from flask import Flask, request, render_template
from math import sqrt
from adiabatic_methane import aft

# create app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # show html form
        return render_template('index.html')
    elif request.method == 'POST':
        # take values from user
        
        T = float(request.form.get('T'))
        P = float(request.form.get('P'))
        lambdaMin = float(request.form.get('lambdaMin'))
        lambdaMax = float(request.form.get('lambdaMax'))
        noPoints = int(request.form.get('noPoints'))
        ch4 = float(request.form.get('ch4'))
        c2h6 = float(request.form.get('c2h6'))
        c3h8 = float(request.form.get('c3h8'))
        co = float(request.form.get('co'))
        co2 = float(request.form.get('co2'))
        h2 = float(request.form.get('h2'))
        #do calculations in external function
        result = aft(T, P, lambdaMin, lambdaMax, noPoints, ch4, c2h6, c3h8, co, co2, h2) #assign returned values
        tad_max, lambda_max = [result[i] for i in [0,1]] #assign values from position
        tad_max = round(tad_max, 2)
        lambda_max = round(lambda_max, 3)
        return render_template ('result.html', tad_max=tad_max, lambda_max=lambda_max)


# run app
if __name__ == '__main__':
    app.run(host='192.168.0.188', port=5005, debug=True)
    #app.run(debug=True)
	
	
