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
            doc.bases.add(data['base'])

            return doc

        elif Documento.objects.filter(titulo=data['title'], doi=data['doi'], revisoes=data['revisao']):
            doc = Documento.objects.get(titulo=data['title'], doi=data['doi'], revisoes=data['revisao'])
            doc.revisoes.add(data['revisao'])
            doc.bases.add(data['base'])



class DocumentoElsevierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Documento
        fields = ['titulo', 'cadastrado_por']

    def save(self, data):
        if not 'citing_paper_count' in data.keys():
            data['citing_paper_count'] = None
        if not 'doi' in data.keys():
            data['doi'] = None

        if not Documento.objects.filter(titulo=data.get('dc:title'), doi=data.get('prism:doi')):
            doc = Documento(
                titulo=data.get('dc:title'),
                autores=data.get('dc:creator'),
                doi=data.get('prism:doi'),
                html_url=data.get('prism:url'),
                revista=data.get('prism:publicationName')
            )
            doc.save()
            doc.revisoes.add(data['revisao'])
            doc.bases.add(data['base'])

            return doc


class NCBISerializer(serializers.ModelSerializer):

    class Meta:
        model = Documento
        fields = ['resumo', 'html_url', 'autores', 'doi', 'palavras_chaves',
                  'data', 'titulo', 'cadastrado_por']

    def save(self, data):
        payload = {k:v for k,v in data.items() if k in self.Meta.fields}

        if not Documento.objects.filter(titulo=data.get('titulo'), doi=data.get('doi')):
            doc = Documento.objects.create(**payload)
            doc.save()
            doc.revisoes.add(data['revisao'])
            doc.bases.add(data['base'])

            return doc

        else:
            doc = Documento.objects.get(titulo=data['titulo'], doi=data['doi'])
            doc.revisoes.add(data['revisao'])
            doc.bases.add(data['base'])