import pdfkit
from django.http import HttpResponse


def html_to_pdf(request):
    url=request.path.replace('/reporting','')
    absolutUrl = request.get_host() +url
    pdfkit_options = {
        'page-size': 'A4',
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'encoding': 'UTF-8',
        'dpi':200,
        'zoom':2,
        'lowquality':False,
    }
    pdf = pdfkit.from_url(absolutUrl, False,options=pdfkit_options)

    response = HttpResponse(pdf, content_type='application/pdf')
    return response