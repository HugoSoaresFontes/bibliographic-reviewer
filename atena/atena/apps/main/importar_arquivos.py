# -*- coding: utf-8 -*-
from .classes_importacao import IEEE_Xplore_Searcher, PubMed_Searcher, PMC_Searcher, ElsevierSearcher
from .serializers import DocumentoSerializerIEEE, NCBISerializer, DocumentoElsevierSerializer
from .models import Base

technology_queryterms = [
    'machine learning', 'deep learning', 'artificial intelligence',
    'neural network'
]

health_queryterms = [
    'coronary artery disease', 'chest pain', 'heart disease', 'MACE',
    'Acute Cardiac Complications'
]

queryterms = [technology_queryterms, health_queryterms]


def importar_arquivos(revisao, base, cadastrante):
    if base == "IEEE Xplore":
        base_artigos = Base.objects.get(id=Base.IEEE_XPLORE)
        ieee_searcher = IEEE_Xplore_Searcher()
        documentos = ieee_searcher.search(queryterms=queryterms,
                                          start_year=1975, content_type="Journals")
        for doc in documentos:
            doc.update({
                'revisao': revisao,
                'cadastrado_por': cadastrante,
                'base': base_artigos
            })
            serializer = DocumentoSerializerIEEE(data=doc)
            serializer.save(doc)

    if base == "Science Direct":
        base_artigos = Base.objects.get(id=Base.SCIENCE_DIRECT)
        elsevier_searcher = ElsevierSearcher(index='scidir')
        documentos = elsevier_searcher.search(queryterms=queryterms,
                                              start_year=2010)
        for doc in documentos:
            doc.update({
                'revisao': revisao,
                'cadastrado_por': cadastrante,
                'base': base_artigos
            })
            serializer = DocumentoElsevierSerializer(data=doc)
            serializer.save(doc)

    if base == "SCOPUS":
        base_artigos = Base.objects.get(id=Base.SCOPUS)
        elsevier_searcher = ElsevierSearcher(index='scopus')
        documentos = elsevier_searcher.search(queryterms=queryterms,
                                              start_year=2010)
        for doc in documentos:
            doc.update({
                'revisao': revisao,
                'cadastrado_por': cadastrante,
                'base': base_artigos
            })
            serializer = DocumentoElsevierSerializer(data=doc)
            serializer.save(doc)

    if base == "PubMed":
        base_artigos = Base.objects.get(id=Base.PUBMED)
        documentos = PubMed_Searcher().search(queryterms=queryterms, max_records=5)
        for doc in documentos:
            doc.update({
                'cadastrado_por': cadastrante.id,
            })
            serializer = NCBISerializer(data=doc)

            if serializer.is_valid():
                novo_documento = serializer.save()
                novo_documento.bases.add(base_artigos)
                novo_documento.revisoes.add(revisao)
            else:
                print(doc['titulo'])

    if base == "PMC":
        base_artigos = Base.objects.get(id=Base.PMC)
        documentos = PMC_Searcher().search(queryterms=queryterms, max_records=5)
        for doc in documentos:
            doc.update({
                'cadastrado_por': cadastrante.id,
            })
            serializer = NCBISerializer(data=doc)

            if serializer.is_valid():
                novo_documento = serializer.save()
                novo_documento.bases.add(base_artigos)
                novo_documento.revisoes.add(revisao)
            else:
                print('invalido:    ',doc['titulo'])
                print(serializer.errors)
