
#!/usr/bin/env python
from flask import Flask, request

# create app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # show html form
        return '''
            <form method="post">
                <input type="text" name="expression_1" />
                <input type="text" name="expression_2" />
                <input type="submit" value="Calculate" />
            </form>
        '''
    elif request.method == 'POST':
        # calculate result
        expression_1 = request.form.get('expression_1')
        expression_2 = request.form.get('expression_2')
        result1 = eval(expression_1)+eval(expression_2)
        result2 = eval(expression_1)-eval(expression_2)
        return 'Suma: {0} \nRóżnica: {1}'.format(result1, result2)

# run app
if __name__ == '__main__':
    app.run(debug=True)