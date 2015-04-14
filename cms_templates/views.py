from django.shortcuts import render
from models import Page
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden

# Necessary imports to work with templates

from django.template.loader import get_template
from django.template import Context

# Create your views here.

@csrf_exempt
def main(request, resource):
    template = False
    content = ""

    if request.user.is_authenticated():
        logged = ("Logged in as " + request.user.username
                + " <a href='/admin/logout/'>Log out</a>")
    else:
        logged = ("Not logged in. "
                + "<a href='/admin/login/?next=/admin/'>Log in</a>")

    if request.method == "GET":
        pthdirs = resource.split("/")
        if pthdirs[0] == "annotated":
            template = True
            if len(pthdirs) > 1:
                resource = pthdirs[1]
            else:
                resource = ""

        try:
            page_entry = Page.objects.get(name=resource)
            content = (logged + "<br/>" + page_entry.page)
        except Page.DoesNotExist:
            if resource == "":
                resource = "Main Page"
            content =  ("Page not found: %s." % resource)

        if template:
            template = get_template("index.html")
            return HttpResponse(template.render(
                                Context({'user': logged,
                                        'title': resource,
                                        'content': content})))
        else:
            return HttpResponse(content)


    elif request.method == "PUT":
        new_entry = Page(name=resource, page=request.body)
        new_entry.save()
        return HttpResponse(logged + "<br/>"
                + "Succesful PUT operation: " + request.body)
    else:
        return HttpResponseForbidden(logged + "<br/>"
            + "Operation not available")