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
from django.shortcuts import redirect
# Create your views here.
"""	

"""

def formulario(request):
	"""
	Esta funcion se encarga de poder decidir si se ha introducido los valores correctos y
	si se cumlpe te lleva a la siguiente pestaña
	"""
	if request.method=="GET":
		dic = {'nombre': request.GET.get("nombre",""),
		"apellido1":request.GET.get("apellido1",""), 
		"apellido2":request.GET.get("apellido2",""),
		"dni":request.GET.get("dni",""),
		"texto":request.GET.get("texto",""),
		"fecha":datetime.today()}
		if validar_formulario(dic)==False:
			return render(request, "formulario/formulario.html",{"dic":dic})
		elif validoDNI(dic["dni"])==False:
			return render(request,"formulario/Error_dni.html",{"dic":dic})
		elif validar_formulario(dic):
			insertar_en_base_de_datos(dic)
			return redirect("/formulario_confirmacion")
	succes_url=reverse_lazy("opciones:opciones") 
	return render(request, "formulario/formulario.html",{"dic":dic})
def insertar_en_base_de_datos(datos):
	"""
	Inserta los datos en la base de datos
	"""
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
	"""
	Valida si el diccionario esta completo y no tiene valores vacios
	"""
	for i in dic.keys():	

		if not dic[i]:
			f = open ("kk.txt", "a")  
			f.write("Error_dni "+str(i)+"\n")
			f.close()
			return False 
	return True

	return True
def validoDNI(dni): 
	"""
	Comprueba que el dni es correcto
	"""
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
	"""
	Funcion que se encarga de generar y enviar un pdf al clientes y el cliente lo descarga seguna 
	la variable descarga
	"""
	template_path = 'formulario/generador_de_pdf.html'
	context = dic
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="report.pdf"' 
	#2response['Content-Disposition'] = 'filename="report.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context) 
	f = open ("log_pdf.txt", "a")  
	f.write(" nuevo--> "+str(descarga)+"\n")
	f.close()
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
	"""
	Api qeu devuelve un pdf con los valores introducidos
	"""
	try:
		if request.method=="GET":
			"""

			Esto sera para la v3
			objeto_dic=cert.objects.get(
				crsf=request.GET.get("crsf")
				)
			f = open ("log_api.txt", "a")  
			f.write(" nuevo--> "+str(objeto_dic)+"\n")
			f.close()
			datos=str(objeto_dic).split("-")
			dic = {'nombre': datos[0],
			"apellido1":datos[1], 
			"apellido2":datos[2],
			"dni":datos[4],
			"texto":datos[3],
			"fecha":datetime.today()}
			"""
			dic = {'nombre': request.GET.get("nombre"),
			"apellido1":request.GET.get("apellido1"), 
			"apellido2":request.GET.get("apellido2"),
			"dni":request.GET.get("dni"),
			"texto":request.GET.get("texto"),
			"fecha":datetime.today()}
			f = open ("log_api.txt", "a")  
			f.write(" nuevo--> "+str(dic)+"\n")
			f.close()
			if (validoDNI(dic["dni"])):
				if request.GET.get("descarga")=="True":
					return usuario_render_pdf_view(request,dic,descarga=True)
				else:
					return usuario_render_pdf_view(request,dic)
				
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

def comprobacion_cookies(dic):
	"""
	Comprueba los cookies de los clientes
	"""
	datos=["nombre","apellido1","apellido2","dni","texto"]
	for i in datos:
		if i not in dic.keys():
			return False
		if not dic[i]:
			return False
	return True

def formulario_confirmacion(request):
	"""
	Comprueba los cookies y el el formulario donde se encuentra y si son correctos le envia el ultimo formulario
	Si son incorrectos envia al cliente al formulario de inicio 
	"""
	if validar_formulario(request.COOKIES) and comprobacion_cookies(request.COOKIES):
		for i in request.COOKIES.keys():

			f = open ("log_prueba_.txt", "a")  
			f.write(" nuevo--> "+i+" "+str(len(request.COOKIES.keys()))+"\n")
			f.close()
		"""
		Aqui tendra que ir una comprobacion elaborada de las cookies
		"""
		return render(request,"formulario/formulario_confirmacion.html")
	f = open ("log_prueba.txt", "a")  
	f.write(" nuevo--> "+str(validar_formulario(request.COOKIES))+" "+str(len(request.COOKIES.keys()))+"\n")
	f.close()
	return redirect("/formulario_v1")


	
	
