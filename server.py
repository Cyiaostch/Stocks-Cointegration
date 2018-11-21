# Framework yang digunakan untuk pembuatan API adalah Flask(Python)
# Autentikasi yang digunakan adalah token based authentication menggunakan JWT(JSON Web Token)
# User akan menukan username dan password dengan token yang memiliki lifetime tertenu(dalam kode ini 30 menit)
# Token nantinya akan disertakan dalam request untuk route yang ingin diproteksi

from flask import Flask, jsonify, request, make_response
import jwt 
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

# Fungsi ini akan digunakan sebagai wrapper untuk route yang memerlukan autentikasi token
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

		if not token:
			return jsonify({'message' : 'Token is missing!'}), 403

		try: 
			data = jwt.decode(token, app.config['SECRET_KEY'])
		except:
			return jsonify({'message' : 'Token is invalid!'}), 403

		return f(*args, **kwargs)

	return decorated

# Fungsi ini digunakan untuk menukar username dan password dengan token
@app.route('/login/<username>/<password>/')
def login(username,password):
	if username=="username" and password=='password':
		token = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}, app.config['SECRET_KEY'])

		return jsonify({'token':token.decode('UTF-8')})

	return jsonify({'token':"INVALID"})

@app.route('/getData/<tickers>/<start_date>/<end_date>/')
@token_required
def get_data(tickers,start_date,end_date):
	#tickers=request.args.get("tickers").split(',')
	#start_date=request.args.get("start_date")
	#end_date=request.args.get("end_date")

	return "Success"
	tickers=tickers.split(',')
	response_parameters=generate_response(tickers,start_date,end_date)
	return jsonify(
		best_parameters=response_parameters[0],
		portofolio=response_parameters[1],
		test_statistics=response_parameters[2],
		p_value=response_parameters[3],
		critical_value_1=response_parameters[4],
		critical_value_5=response_parameters[5],
		critical_value_10=response_parameters[6])

def generate_response(tickers,start_date,end_date):
	return range(7)
	stocks_data=get_data(tickers,start_date,end_date)
    
	compiled_stocks_data=compile_data(stocks_data,"Close",tickers)
    
	optimized_portofolio=optimize_portofolio(tickers,0.01,100)
    
	best_parameters,portofolio=optimized_potofolio
    
	dicky_fuller_statistics=stationary_test(best_parameters,portofolio)
	test_statistics=dicky_fuller_statistics[0]
	p_value=dicky_fuller_statistics[1]
	critical_value_1=dicky_fuller_statistics[4]['1%']
	critical_value_5=dicky_fuller_statistics[4]['5%']
	critical_value_10=dicky_fuller_statistics[4]['10%']
    
	return best_parameters,portofolio,test_statistics,p_value,critical_value_1,critical_value_5,critical_value_10

if __name__ == '__main__':
	app.run(debug=True)
