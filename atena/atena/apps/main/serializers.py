from rest_framework import serializers
from bs4 import BeautifulSoup as bsoup
from datetime import datetime

from contas.models import Usuario
from .models import Documento

class DocumentoSerializerIEEE(serializers.ModelSerializer):
	class Meta:
		model = Documento
		fields = ['titulo', 'cadastrado_por']

	def save(self, data):
		# Falta a data por questões de formato
		if not 'citing_paper_count' in data.keys():
		 	data['citing_paper_count'] = None
		if not 'doi' in data.keys():
		 	data['doi'] = None
		if not Documento.objects.filter(titulo=data['title'], doi=data['doi']):
			doc = Documento(
				titulo=data['title'],
				resumo=data['abstract'],
				resumo_url=data['abstract_url'],
				autores=data['authors'],
				citado_papers=data['citing_paper_count'],
				doi=data['doi'],
				palavras_chaves=data['title'],
				pdf_url=data['pdf_url'],
				rank=data['rank'],
				cadastrado_por=data['cadastrado_por']
			)
			doc.save()
			doc.revisoes.add(data['revisao'])
			return doc

class PubMedSerializer(serializers.ModelSerializer):

	class Meta:
		model = Documento
		fields = ['resumo', 'resumo_url', 'autores', 'doi', 'palavras_chaves',
				  'data', 'titulo']
