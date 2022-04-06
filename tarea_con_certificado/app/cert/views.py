from django.shortcuts import render
from csv import field_size_limit
from dataclasses import fields
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.urls import reverse_lazy
from django.views.generic import TemplateView ,ListView,CreateView,DeleteView,UpdateView,DetailView
# Create your views here.
from .models import *
from  .models import cert
from xhtml2pdf import pisa
from datetime import datetime
from django.template.loader import get_template

# Create your views here.
"""

"""

def formulario(request):  
	
	if request.method=="GET":
		formulario=[]
		formulario.append(request.GET.get("nombre",""))
		formulario.append(request.GET.get("apellido1",""))
		formulario.append(request.GET.get("apellido2",""))
		formulario.append(request.GET.get("dni",""))
		formulario.append(request.GET.get("texto",""))
		f = open ("kk.txt", "a") 
		
		for i in formulario:
			f.write(str(i)+"\n")
		
			
		f.close()
		if validoDNI(formulario[3])==False:
			return render(request,"formulario/Error.html")
		elif validar_formulario(formulario):
			return usuario_render_pdf_view(request,formulario)
	succes_url=reverse_lazy("opciones:opciones") 
	return render(request, "formulario/formulario.html")
def validar_formulario(formulario):
	for i in formulario:
		if i==False:
			return False
	return True
			


 

def validoDNI(dni): 
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    dig_ext = "XYZ"
    reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
    numeros = "1234567890"
    dni = dni.upper()
    if len(dni) == 9:
        dig_control = dni[8]
        dni = dni[:8]
        if dni[0] in dig_ext:
            dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
        return len(dni) == len([n for n in dni if n in numeros]) \
            and tabla[int(dni)%23] == dig_control
    return False

def usuario_render_pdf_view(request,lista):
    

    template_path = 'formulario/generador_de_pdf.html'
    context = {'nombre': lista[0],"apellido1":lista[1],"apellido2":lista[2],"dni":lista[3],"texto":lista[4],"fecha":datetime.today()}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"' 
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context) 

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response