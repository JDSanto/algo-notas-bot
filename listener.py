import requests
import json


def get_page(url):
	try:
		htmlContent = requests.get(url)
		arr = htmlContent.text.encode('utf-8').split('\n')
		return arr
	except BaseException as e:
		print e


# Obtiene las notas de la pagina del sistema de entregas
# y las devuelve en forma de diccionario
def get_grades(url):
	arr = get_page(url)
	grades = {}
	for ind, obj in enumerate(arr):
		if obj == "  <tr>":
			key = arr[ind + 1][8:-5]
			val = arr[ind + 2][8:-5]
			if key != '':
				grades[key] = val
	return json.dumps(grades)

