from django.shortcuts import render
from django.http import HttpResponse
from django import forms


from . import util
from markdown2 import markdown


class EditPageForm(forms.Form):
    title_form = forms.CharField(label="Title")
    info_form = forms.CharField(label="Article", widget=forms.Textarea(attrs={'class': "form-control"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    info = util.get_entry(title)
    if info is not None:
        return render(request, "encyclopedia/wiki.html", {
            'title': title,
            'info': markdown(info)
        })


def search(request):
    list_files = util.list_entries()
    q = request.GET.get('q', '')

    # Try to find a file with that name and redirect to wiki pages if found
    if q in list_files:
        info = util.get_entry(q)
        if info is not None:
            return render(request, "encyclopedia/wiki.html", {
                'title': q,
                'info': markdown(info)
            })

    # looking for files with a keyword
    q = q.lower()
    search_results = [file for file in list_files if q in file.lower()]
    return render(request, "encyclopedia/search.html", {
        'results': search_results
    })


def random(request):
    pass
    return HttpResponse.Redirect((reverse))


def edit(request, title):
    if request.method == 'POST':
        pass
    info_md = util.get_entry(title)
    if info_md is not None:
        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'info_md': info_md,
            'form': EditPageForm
        })