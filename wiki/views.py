from djwiki.wiki.models import Page, Tag
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django import forms

# Search Form
class SearchForm(forms.Form):
	text = forms.CharField(label="")
	search_content = forms.BooleanField(label="Search content", required=False)

""" LEGACY
def search_page(request):
	if request.method == "POST":
		f = SearchForm(request.POST)
		if not f.is_valid():
			return render_to_response("search.html", {"form":f}, RequestContext(request))
		else:
			try:
				pages = Page.objects.filter(name__contains = f.cleaned_data["text"])
				contents = []
				#if f.cleaned_data["search_content"]:
				#	contents = Page.objects.filter(content__contains = f.cleaned_data["text"])
				return render_to_response("search.html", {"form":f, "pages": pages, "contents": contents}, RequestContext(request))
			except Page.DoesNotExist:
				f = SearchForm()
				show_searchbox = True
				noresults = True
				return render_to_response("search.html", {"noresults": noresults, "show_searchbox": show_searchbox, "form":f}, RequestContext(request))
			
	f = SearchForm()
	show_searchbox = True
	return render_to_response("search.html", {"show_searchbox": show_searchbox, "form":f}, RequestContext(request))
"""	
#specialPages = {"SearchPage": search_page}

def view_page(request, page_name):
	if request.method == "POST":
		f = SearchForm(request.POST)
		variables = search_page(request, f)
		return render_to_response("search.html", variables)
	#if page_name in specialPages:
	#	return specialPages[page_name](request)
	
	f = SearchForm()
	try:
		page = Page.objects.get(pk=page_name)
		tags = page.tags.all()
	except Page.DoesNotExist:
		return render_to_response("create.html", {"page_name": page_name, "form":f}, RequestContext(request))
	content = page.content
	return render_to_response("view.html", {"page_name": page_name, "content": content, "tags": tags, "form":f}, RequestContext(request))
		
def edit_page(request, page_name):
	if request.method == "POST":
		f = SearchForm(request.POST)
		variables = search_page(request, f)
		return render_to_response("search.html", variables)
	f = SearchForm()
	try:
		page = Page.objects.get(pk=page_name)
		content = page.content
		tags = " ".join([tag.name for tag in page.tags.all()])
	except Page.DoesNotExist:
		content = ""
		tags = ""
	return render_to_response("edit.html", {"page_name": page_name, "content": content, "tags": tags, "form":f}, RequestContext(request))
	
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
		page.save()
		for tag in tag_list:
			page.tags.add(tag)
	page.save()
	return HttpResponseRedirect("/wiki/page/" + page_name + "/")
	
def view_tag(request, tag_name):
	if request.method == "POST":
		f = SearchForm(request.POST)
		variables = search_page(request, f)
		return render_to_response("search.html", variables)
	f = SearchForm()
	tag = Tag.objects.get(pk=tag_name)
	pages = tag.page_set.all()
	return render_to_response("tags.html", {"tag_name": tag_name, "pages": pages, "form": f}, RequestContext(request))
	
def search_page(request, f):	
	if not f.is_valid():
		show_searchbox = True
		variables = RequestContext(request, {
			"show_searchbox": show_searchbox,
			"form": f
		})
		return variables
	else:
		pages = Page.objects.filter(name__contains = f.cleaned_data["text"])
		if f.cleaned_data["search_content"]:
			contents = Page.objects.filter(content__contains = f.cleaned_data["text"])
		else:
			contents = Page.objects.none()
		if pages.exists() or contents.exists():
			variables = RequestContext(request, {
				"form": f,
				"pages": pages,
				"contents": contents
			})
			return variables
		else:
			f = SearchForm()
			show_searchbox = True
			noresults = True
			variables = RequestContext(request, {
				"noresults": noresults,
				"show_searchbox": show_searchbox,
				"form": f
			})
			return variables