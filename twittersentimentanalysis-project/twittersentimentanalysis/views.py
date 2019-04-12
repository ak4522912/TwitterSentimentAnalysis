from django.http import HttpResponse
from django.shortcuts import render
from . import polarityanalysis
from django.template import Context, loader
import datetime
import csv
import operator
import os

def polar(request):
	query=request.GET['query']
	count=request.GET['select']

	Test=polarityanalysis.main(query,count)
	csvout2(Test)
	
	return render(request,'polar.html',{'Test':Test})

def analyser(request):
    return render(request,'index.html')

def archive(request):
    file_list=filesfromarchive()
    return render(request,'Archive.html',{'file_list':file_list})

def filesfromarchive():
    path="static/archive"  # insert the path to your directory   
    file_list =os.listdir(path)   
    return ( file_list)

def csvout(Test):
	response = HttpResponse(content_type='text/csv')
	file_name = "static/archive/Sentiment_Analysis_of_{}_Tweets_About_{}_at_{}.csv".format(Test.count, Test.query,datetime.datetime.now().date())
	response['Content-Disposition'] = 'attachment; filename=file_name'
	writer = csv.writer(response)
	writer.writerow(['Tweet','Sentiment'])
	for word in Test.list1:
		writer.writerow([word,'positive'])
	for word in Test.list2:
		writer.writerow([word,'negative'])
 
	return response

def csvout2(Test):
	file_name = "static/archive/Sentiment_Analysis_of_{}_Tweets_About_{}_at_{}.csv".format(Test.count, Test.query,datetime.datetime.now().date())
	

	
	with open(file_name, 'w', newline='') as csvfile:
   		csv_writer = csv.DictWriter(
       	f=csvfile,
       	fieldnames=["Tweet", "Sentiment"]
  		 )
   		csv_writer.writeheader()
   		for tweet in Test.list1:
   			tidy_tweet = tweet.strip().encode('ascii', 'ignore')
   			csv_writer.writerow({
           		'Tweet': tidy_tweet,
           		'Sentiment': 'positive'
       })
   		for tweet in Test.list2:
   			tidy_tweet = tweet.strip().encode('ascii', 'ignore')
   			csv_writer.writerow({
           		'Tweet': tidy_tweet,
           		'Sentiment': 'negative'
       })
   		csvData = [['Percentage of positive tweets', Test.positive], ['Percentage of negative tweets', Test.negative], ['Percentage of neutral tweets', Test.neutral]]
   		writer = csv.writer(csvfile)
   		writer.writerows(csvData)
	csvfile.close()

# def some_view(Test):
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

#     # The data is hard-coded here, but you could load it from a database or
#     # some other source.
#     csv_data = (
#         ('First row', 'Foo', 'Bar', 'Baz'),
#         ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
#     )

#     t = loader.get_template('my_template_name.txt')
#     c = {
#         'data': 'abc',
#     }
#     response.write(t.render(c))
    # return response
 