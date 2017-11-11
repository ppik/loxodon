from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from logos.forms import LogoAnalyzeForm
from logos.models import LogoAnalyze
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from logos.keras_run import get_prediction
import json

with open('models/carnet-2017-11-11T14:57:39.955932-classes.json') as data_file:
    classes_json = json.load(data_file)

classes = [c.replace('_', ' ').title() for c in classes_json.keys()]

def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = LogoAnalyzeForm(request.POST, request.FILES)
        if form.is_valid():
            logoanalyze = form.save(commit=False)
            print(logoanalyze.video)

            # Get logo names / confidence scores
            brand, confidence = get_prediction(logoanalyze.video)

            logoanalyze.precision = confidence #"Enter your precision here"
            logoanalyze.suggested_logo_name = brand #"Enter your suggested logo name here"
            # Redirect to index page
            logoanalyze.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = LogoAnalyzeForm()  # A empty, unbound form

    # Load documents for the list page
    logoanalyzes = LogoAnalyze.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'index.html',
        {'logoanalyzes': logoanalyzes, 'form': form, 'classes': classes}
    )
