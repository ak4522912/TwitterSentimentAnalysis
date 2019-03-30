from django.http import HttpResponse
from django.shortcuts import render
from . import polarityanalysis

import operator

def polar(request):
	query=request.GET['query']
	list1=polarityanalysis.main(query)
	return render(request,'polar.html',{'list1':list1})
def analyser(request):
    return render(request,'index.html')
 



 