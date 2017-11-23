from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from logos.forms import LogoAnalyzeForm
from logos.models import LogoAnalyze
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from logos.keras_run import get_prediction
import json
from django.core.files.storage import FileSystemStorage
from time import sleep

with open('models/car-inceptionv3-2017-11-22_431-classes.json') as data_file:
    classes_json = json.load(data_file)

classes = [c.replace('_', ' ').title() for c in classes_json.keys()]

def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = LogoAnalyzeForm(request.POST, request.FILES)
        if form.is_valid():
            logoanalyze = form.save()
            logoanalyze.save()

            # Get logo names / confidence scores
            values, class_names = get_prediction(logoanalyze.video)

            LogoAnalyze.objects.filter(video=logoanalyze.video).update(logo_name_1 = class_names[0],
                                                                 precision_1 = values[0],
                                                                 logo_name_2 = class_names[1],
                                                                 precision_2 = values[1],
                                                                 logo_name_3 = class_names[2],
                                                                 precision_3 = values[2])


            # Redirect to index page
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
