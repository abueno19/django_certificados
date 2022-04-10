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
from io import StringIO, BytesIO

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
		dic = {'nombre': request.GET.get("nombre",""),
		"apellido1":request.GET.get("apellido1",""), 
		"apellido2":request.GET.get("apellido2",""),
		"dni":request.GET.get("dni",""),
		"texto":request.GET.get("texto",""),
		"fecha":datetime.today()}
		if nada(formulario):
			return render(request, "formulario/formulario.html",{"dic":dic})
		elif validoDNI(dic["dni"])==False:
			return render(request,"formulario/Error_dni.html",{"dic":dic})
		elif validar_formulario(dic):
			insertar_en_base_de_datos(dic)
			return usuario_render_pdf_view(request,dic)
	succes_url=reverse_lazy("opciones:opciones") 
	return render(request, "formulario/formulario.html",{"dic":dic})
def insertar_en_base_de_datos(datos):
	f = open ("log.txt", "a")  
	f.write("Error"+str(datos)+"\n")
	f.close()
	cert.objects.create(
		name=datos["nombre"],
		last_name1=datos["apellido1"],
		last_name2=datos["apellido2"],
		texto=datos["texto"],
		dni=datos["dni"],

		)




def validar_formulario(dic):
	for i in dic.keys():	

		if not dic[i]:
			f = open ("kk.txt", "a")  
			f.write("Error_dni "+str(i)+"\n")
			f.close()
			return False 
	return True
def nada(lista):
	for i in lista:

		if i:
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

def usuario_render_pdf_view(request,dic,descarga=False):
    

	template_path = 'formulario/generador_de_pdf.html'
	context = dic
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="report.pdf"' 
	#2response['Content-Disposition'] = 'filename="report.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context) 

    # create a pdf
	if descarga:
		result = BytesIO()
		pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
		if not pdf.err:
		# Force pdf download
			response = HttpResponse(result.getvalue(), content_type='application/force-download')
			response['Content-Disposition'] = 'attachment; filename="borrador.pdf"'

			return response
	else:
		pisa_status = pisa.CreatePDF(
		html, dest=response)

    # if error then show some funy view
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response
def prueba_api(request):
	try:
		if request.method=="GET":
			f = open ("log_api.txt", "a")  
			f.write(" nuevo--> "+str(request.GET)+"\n")
			f.close()
			dic = {'nombre': request.GET.get("nombre",""),
			"apellido1":request.GET.get("apellido1",""), 
			"apellido2":request.GET.get("apellido2",""),
			"dni":request.GET.get("dni",""),
			"texto":request.GET.get("texto",""),
			"fecha":datetime.today()}
			f = open ("log_api.txt", "a")  
			f.write(" nuevo--> "+str(request.GET)+"\n")
			f.close()
			if (validoDNI(dic["dni"])):
				return usuario_render_pdf_view(request,dic,descarga=True)
		else:
			f = open ("log_api.txt", "a")  
			f.write(" nuevo--> "+str("No ha entrado")+"\n")
			f.close()
	except:
		f = open ("log_api.txt", "a")  
		f.write(" nuevo--> "+str("No ha entrado")+"\n")
		f.close()
		return render(request,"Error")

	return render(request,"Error")

	
	
