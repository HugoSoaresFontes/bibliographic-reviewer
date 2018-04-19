from rest_framework import serializers
from bs4 import BeautifulSoup as bsoup
from datetime import datetime
from functools import reduce

from contas.models import Usuario
from .models import Documento, Base
import dateparser

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

        else:
            doc = Documento.objects.get(titulo=data['title'], doi=data['doi'])
            doc.revisoes.add(data['revisao'])
            doc.bases.add(data['base'])

            return doc


class DocumentoElsevierSerializer(serializers.ModelSerializer):
    def __init__(self, base, **kwargs):
        super().__init__(**kwargs)
        self.base = base

    class Meta:
        model = Documento
        fields = ['titulo', 'cadastrado_por']

    def save(self, data):
        if not 'citing_paper_count' in data.keys():
            data['citing_paper_count'] = None
        if not 'doi' in data.keys():
            data['doi'] = None

        try:
            if self.base == Base.SCIENCE_DIRECT:
                authors = data['authors']['author']
                authors = reduce((lambda x, y: f"{x}; {y['given-name']} {y['surname']}"), authors[1:],
                                 f"{authors[0]['given-name']} {authors[0]['surname']}")
            if self.base == Base.SCOPUS:
                authors = data.get('dc:creator')
        except:
            authors = data.get('dc:creator')

        try:
            if self.base == Base.SCIENCE_DIRECT:
                date = datetime.strptime(data['prism:coverDate'][0]['$'], '%Y-%m-%d')
            elif self.base == Base.SCOPUS:
                date = datetime.strptime(data['prism:coverDate'], '%Y-%m-%d')
        except:
            if 'prism:coverDisplayDate' in data:
                date = dateparser.parse(data['prism:coverDisplayDate'])


        if not Documento.objects.filter(titulo=data.get('dc:title'), doi=data.get('prism:doi')):
            doc = Documento(
                titulo=data.get('dc:title'),
                autores=authors,
                doi=data.get('prism:doi'),
                data=date,
                html_url=data.get('prism:url'),
                revista=data.get('prism:publicationName')
            )
            doc.save()
            doc.revisoes.add(data['revisao'])
            doc.bases.add(data['base'])

            return doc

        else:
            doc = Documento.objects.get(titulo=data.get('dc:title'), doi=data.get('prism:doi'))
            doc.revisoes.add(data['revisao'])
            doc.bases.add(data['base'])

            return doc


class DocumentoSpringerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = ['titulo', 'cadastrado_por']

    def save(self, data):
        if not 'doi' in data.keys():
            data['doi'] = None

        try:
            url = [x['value'] for x in data.get('url') if x['format'] == 'html'][0]
        except:
            url = [x['value'] for x in data.get('url')][0]

        if not Documento.objects.filter(titulo=data.get('title'), doi=data.get('doi')):
            l = lambda x, y: f'{x}; {y["creator"]}'
            lista = data.get('creators')
            try:
                autores = reduce(l, lista[1:], lista[0]['creator'])
            except:
                autores = None

            doc = Documento(
                autores=autores,
                titulo=data['title'],
                doi=data['doi'],
                revista=data['publicationName'],
                html_url=url,
                data=datetime.strptime(data['publicationDate'], '%Y-%m-%d'),
                resumo=data['abstract']
            )
            doc.save()
            doc.revisoes.add(data['revisao'])
            doc.bases.add(data['base'])

            return doc

        else:
            doc = Documento.objects.get(titulo=data['title'], doi=data['doi'])
            doc.revisoes.add(data['revisao'])
            doc.bases.add(data['base'])


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