from wiki.models import Page, Tag
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django import forms

# Search Form
class SearchForm(forms.Form):
	text = forms.CharField(label="")
	search_content = forms.BooleanField(label="Search content", required=False)
	
class NewPageForm(forms.Form):
	text = forms.CharField(label="", max_length=100)

def view_page(request, page_name):
	if request.method == "POST":
		if "searchbar" in request.POST:
			f = SearchForm(request.POST)
			np = NewPageForm()
			variables = search_page(request, f, np)
			return render_to_response("search.html", {"newpageform": np}, variables)
		elif "newpage" in request.POST:
			f = SearchForm(request.POST)
			np = NewPageForm()
			newpagename = request.POST["text"]
			try: 
				page= Page.objects.get(pk=newpagename)
				tags = page.tags.all()
				content = page.content
				return render_to_response("view.html", {"page_name" : newpagename, "content": content, "tags":tags, "form":f, "newpageform": np}, RequestContext(request))
			except Page.DoesNotExist:
				return render_to_response("create.html", {"newpagename": newpagename, "form": f, "newpageform": np}, RequestContext(request))
				
	f = SearchForm()
	np = NewPageForm()
	try:
		page = Page.objects.get(pk=page_name)
		tags = page.tags.all()
	except Page.DoesNotExist:
		return render_to_response("create.html", {"page_name": page_name, "form":f, "newpageform": np}, RequestContext(request))
	content = page.content
	return render_to_response("view.html", {"page_name": page_name, "content": content, "tags": tags, "form":f, "newpageform": np}, RequestContext(request))
		
def edit_page(request, page_name):
	if request.method == "POST":
		if "searchbar" in request.POST:
			f = SearchForm(request.POST)
			np = NewPageForm()
			variables = search_page(request, f, np)
			return render_to_response("search.html", variables)
		elif "newpage" in request.POST:
			f = SearchForm(request.POST)
			np = NewPageForm()
			newpagename = request.POST["text"]
			try: 
				page= Page.objects.get(pk=newpagename)
				tags = page.tags.all()
				content = page.content
				return render_to_response("view.html", {"page_name" : newpagename, "content": content, "tags":tags, "form":f, "newpageform": np}, RequestContext(request))
			except Page.DoesNotExist:
				return render_to_response("create.html", {"newpagename": newpagename, "form": f, "newpageform": np}, RequestContext(request))
	f = SearchForm()
	np = NewPageForm()
	try:
		page = Page.objects.get(pk=page_name)
		content = page.content
		tags = " ".join([tag.name for tag in page.tags.all()])
	except Page.DoesNotExist:
		content = ""
		tags = ""
	return render_to_response("edit.html", {"page_name": page_name, "content": content, "tags": tags, "form":f, "newpageform": np}, RequestContext(request))
	
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
		if "searchbar" in request.POST:
			f = SearchForm(request.POST)
			np = NewPageForm()
			variables = search_page(request, f, np)
			return render_to_response("search.html", variables)
		elif "newpage" in request.POST:
			f = SearchForm(request.POST)
			np = NewPageForm()
			newpagename = request.POST["text"]
			try: 
				page= Page.objects.get(pk=newpagename)
				tags = page.tags.all()
				content = page.content
				return render_to_response("view.html", {"page_name" : newpagename, "content": content, "tags":tags, "form":f, "newpageform": np}, RequestContext(request))
			except Page.DoesNotExist:
				return render_to_response("create.html", {"newpagename": newpagename, "form": f, "newpageform": np}, RequestContext(request))
	f = SearchForm()
	tag = Tag.objects.get(pk=tag_name)
	pages = tag.page_set.all()
	return render_to_response("tags.html", {"tag_name": tag_name, "pages": pages, "form": f}, RequestContext(request))
	
def search_page(request, f, np):	
	if not f.is_valid():
		show_searchbox = True
		variables = RequestContext(request, {
			"show_searchbox": show_searchbox,
			"form": f,
			"newpageform": np,
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
				"newpageform": np,
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
				"form": f,
				"newpageform": np,
			})
			return variables