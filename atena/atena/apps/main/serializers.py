from rest_framework import serializers

from contas.models import Usuario
from .models import Documento

class DocumentoSerializerIEEE(serializers.ModelSerializer):
	class Meta:
		model = Documento
		fields = ['titulo', 'cadastrado_por']

	def save(self, data):
		
		if not 'citing_paper_count' in data.keys():
		 	data['citing_paper_count'] = None

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
		# Falta add o documento a revisão
		return doc