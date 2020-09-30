from flask import Flask, request, render_template, make_response
import support_methods as wc
app = Flask(__name__, template_folder="../template", static_folder="../template")




@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('index.html')
	

@app.route('/view_graphics', methods=['GET', 'POST'])
def entryPoint():
	keyword = request.form.get('keyword')
	wc.scrapper_main([keyword, 'prova'])
	return render_template('view.html')

if __name__ == '__main__':
	#app.run(host='0.0.0.0',port=8080, debug=False)
	app.run(debug=True)

#"https://my.customscoop.com/reports/viewclips/reportview.cfm?clipReportTemplateId=24&savedNewsletterName=&savedNewsletterDescription=&start=09%2F01%2F20&daySpan=&end=09%2F27%2F20&hourSpan=&kwid=363205&kwid=361303&kwid=363976&kwid=363975&kwid=361298&kwid=361299&kwid=361300&kwid=361301&ClipRatingList=181983&HeadlineText=&OrderBy=time&maxResults=&CompeteGreater=&CompeteLess=&alexaGreater=&alexaLess=&clipSearchCirculationSelect=-1&circulationGreater=&circulationLess=&autotaguserfolderid=&nowait=1"