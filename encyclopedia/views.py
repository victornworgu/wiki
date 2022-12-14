from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
from . import msgs
from random import choice
from markdown2 import Markdown

class NewWikiForm(forms.Form):
	title = forms.CharField(label="Wiki Title", widget=forms.TextInput(attrs={'autofocus': '', 'placeholder':'Enter wiki title here'}))
	content = forms.CharField(label="Wiki Content", widget=forms.Textarea(attrs={'placeholder':'Enter wiki content here. Markdown format supported'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def view_entry(request, title):
	if title in util.list_entries():
		converter = Markdown()
		product = converter.convert(util.get_entry(title))
		return render(request, "encyclopedia/entry.html", {"entry": product, "title": title})
	else:
		return render(request, "encyclopedia/entry.html", {"error": msgs.view_error, "title": "Page not found"})

def edit(request, title):
	form_data = {"title": title, "content": util.get_entry(title)}
	form = NewWikiForm(form_data)
	if request.method == "POST":
		edited_wiki = NewWikiForm(request.POST)
		if edited_wiki.is_valid():
			title = edited_wiki.cleaned_data.get('title')
			content = edited_wiki.cleaned_data.get('content')

			if title in util.list_entries() and content == util.get_entry(title):
				return render(request, "encyclopedia/edit.html", {"form": form, "title": title, "error": msgs.edit_error})
			else:
				util.save_entry(title, content)
				return redirect('viewentry', title=title)


	if title in util.list_entries():
		return render(request, "encyclopedia/edit.html", {"form": form, "title": title})

def search(request):
	query = request.POST.get("q")
	entries = util.list_entries()
	if query in entries:
		return redirect('viewentry', title=query)
	else:
		if query and query.strip():
			filtered = [x for x in entries if query in x]
			"""filtered = []
			for x in entries:
				if query in x:
					filtered.append(x)"""
			return render(request, "encyclopedia/search.html", {"search_results": filtered, "query": query, "error": msgs.search_error})
	return render(request, "encyclopedia/index.html", {"entries": entries})

def addnew(request):
	if request.method == "POST":
		new_wiki = NewWikiForm(request.POST)
		if new_wiki.is_valid():
			title = new_wiki.cleaned_data.get('title')
			content = new_wiki.cleaned_data.get('content')
			if title in util.list_entries():
				return render(request, "encyclopedia/addnew.html", {"form": new_wiki, "error": msgs.add_error})
			else:
				util.save_entry(title, content)
				return redirect('viewentry', title=title)

	return render(request, "encyclopedia/addnew.html", {"form": NewWikiForm})

def random(request):
	random_entry = choice(util.list_entries())
	return redirect('viewentry', title=random_entry)
