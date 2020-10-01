from flask import Flask, request, render_template, make_response
import support_methods as wc
import os, shutil
app = Flask(__name__, template_folder="../template", static_folder="../template")


def delete_wc():
	folder = './template/wordClouds'
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('index.html')
	

@app.route('/view_graphics', methods=['GET', 'POST'])
def entryPoint():
	keyword = request.form.get('keyword')
	if keyword == None:
		delete_wc()
		words = request.form.get('update')
		words = words.replace(' ', '')
		list_words = words.split(',')
		indirizzo_update = wc.update_wc('update', list_words)
		return render_template('view.html', graph = indirizzo_update)
	indirizzo = wc.scrapper_main([keyword, 'wc'])
	return render_template('view.html', graph = indirizzo)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8050, debug=True)
	#app.run(debug=True)

#"https://my.customscoop.com/reports/viewclips/reportview.cfm?clipReportTemplateId=24&savedNewsletterName=&savedNewsletterDescription=&start=09%2F01%2F20&daySpan=&end=09%2F27%2F20&hourSpan=&kwid=363205&kwid=361303&kwid=363976&kwid=363975&kwid=361298&kwid=361299&kwid=361300&kwid=361301&ClipRatingList=181983&HeadlineText=&OrderBy=time&maxResults=&CompeteGreater=&CompeteLess=&alexaGreater=&alexaLess=&clipSearchCirculationSelect=-1&circulationGreater=&circulationLess=&autotaguserfolderid=&nowait=1"