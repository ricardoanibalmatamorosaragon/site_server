from flask import Flask, request, render_template, make_response
import support_methods as wc
app = Flask(__name__, template_folder="../template", static_folder="../template")




@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('index.html')
	

@app.route('/view_graphics', methods=['GET', 'POST'])
def entryPoint():
	keyword = request.form.get('keyword')
	#wc.scrapper_main([keyword, 'prova'])
	return render_template('view.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8080, debug=False)
	#app.run(debug=True)
