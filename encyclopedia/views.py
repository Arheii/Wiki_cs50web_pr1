from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms


from . import util
from markdown2 import markdown
from random import choice

class EditPageForm(forms.Form):
    title_form = forms.CharField(widget=forms.TextInput({"class":"form-control font-weight-bold"}))
    info_form = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control", 'placeholder': "Use markdown syntax"}))


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
    else:
        return render(request, "encyclopedia/error.html", {
            'message': f"Wiki page for {title} not found",
            'info': f"but you can <a href={reverse('pedia:new')}>create</a> new"
             },
             status=404)



def search(request):
    list_files = util.list_entries()
    q = request.GET.get('q', '')

    # Try to find a file with that name and redirect to wiki pages if found
    if q in list_files:
        return HttpResponseRedirect(reverse("pedia:wiki", kwargs={'title':q}))

    # looking for files with a keyword
    search_results = [file for file in list_files if q.lower() in file.lower()]
    return render(request, "encyclopedia/search.html", {
        'results': search_results,
        'search_query': q
    })


def random(request):
    page = choice(util.list_entries())
    return HttpResponseRedirect(reverse("pedia:wiki", kwargs={'title':page}))


def edit(request, title):
    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['info_form']
            util.save_entry(title, content) # Save to file
            return HttpResponseRedirect(reverse("pedia:wiki", kwargs={'title':title}))
        else:
            return render(request, "encyclopedia/edit.html", {
                'title': title,
                'form': form
            })

    info_md = util.get_entry(title)
    if info_md is None:
        # Redirect to create new page
        return HttpResponseRedirect(reverse("pedia:new"))

    # create and fill form fields. Disable to edit title form.
    form = EditPageForm(initial={'title_form': title, 'info_form': info_md})
    form.fields['title_form'].widget.attrs['readonly'] = True
    return render(request, "encyclopedia/edit.html", {
        'title': title,
        'form': form
    })


def new(request):
    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['info_form']
            title = form.cleaned_data['title_form']
            if title not in util.list_entries():
                util.save_entry(title, content) # Save to file
                return HttpResponseRedirect(reverse("pedia:wiki", kwargs={'title':title}))
            else:
                return render(request, "encyclopedia/error.html", {
                    'message': f"Page <b>{title}</b> already exists",
                    'info': f"you can visit <a href={reverse('pedia:wiki', kwargs={'title':title})}>{title}</a>"
                    },
                    status=404)
        else:
            return render(request, "encyclopedia/new.html", {'form': form})

    return render(request, "encyclopedia/new.html", {'form': EditPageForm()})
