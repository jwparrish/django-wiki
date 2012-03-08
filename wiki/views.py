from djwiki.wiki.models import Page, Tag
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django import forms

class SearchForm(forms.Form):
	text = forms.CharField(label="Enter search term")
	search_content = forms.BooleanField(label="Search content", required=False)

def search_page(request):
	if request.method == "POST":
		f = SearchForm(request.POST)
		if not f.is_valid():
			return render_to_response("search.html", {"form":f}, RequestContext(request))
		else:
			pages = Page.objects.filter(name__contains = f.cleaned_data["text"])
			contents = []
			if f.cleaned_data["search_content"]:
				contents = Page.objects.filter(content__contains = f.cleaned_data["text"])
			return render_to_response("search.html", {"form":f, "pages": pages, "contents": contents}, RequestContext(request))
			
	f = SearchForm()
	return render_to_response("search.html", {"form":f}, RequestContext(request))

specialPages = {"SearchPage": search_page}

def view_page(request, page_name):
	if page_name in specialPages:
		return specialPages[page_name](request)
	try:
		page = Page.objects.get(pk=page_name)
		tags = page.tags.all()
	except Page.DoesNotExist:
		return render_to_response("create.html", {"page_name": page_name})
	content = page.content
	return render_to_response("view.html", {"page_name": page_name, "content": content, "tags": tags})
		
def edit_page(request, page_name):
	try:
		page = Page.objects.get(pk=page_name)
		content = page.content
	except Page.DoesNotExist:
		content = ""
	return render_to_response("edit.html", {"page_name": page_name, "content": content}, RequestContext(request))
	
def save_page(request, page_name):
	content = request.POST["content"]
	tag_list = []
	if "tags" in request.POST:
		tags = request.POST["tags"]
		tag_list = [Tag.objects.get_or_create(name=tag)[0] for tag in tags.split()]
		
	try:
		page = Page.objects.get(pk=page_name)
		page.content = content
		for tag in tag_list:
			page.tags.add(tag)
	except Page.DoesNotExist:
		page = Page(name=page_name, content=content)
		for tag in tag_list:
			page.tags.add(tag)
	page.save()
	return HttpResponseRedirect("/wiki/page/" + page_name + "/")