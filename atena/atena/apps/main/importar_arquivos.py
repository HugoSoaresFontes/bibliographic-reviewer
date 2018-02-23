# -*- coding: utf-8 -*-
from .classes_importacao import IEEE_Xplore_Searcher
from .serializers import DocumentoSerializerIEEE
from .models import Documento

technology_queryterms = [
    'machine learning', 'deep learning', 'artificial intelligence',
    'neural network', 'scoring system'
]

health_queryterms = [
    'coronary artery disease', 'chest pain', 'heart disease', 'MACE',
    'Acute Cardiac Complications'
]

queryterms = [technology_queryterms, health_queryterms]

def importar_arquivos(revisao, base, cadastrante):
    if base == "IEEE Xplore":
        ieee_searcher = IEEE_Xplore_Searcher()
        print(cadastrante)
        documentos = ieee_searcher.search(queryterms=queryterms,
                                        start_year=1975, content_type="Journals")
        for doc in documentos[:10]: 
        	doc.update({
        		'revisao': revisao, 
        		'cadastrado_por': cadastrante
        		})
        	serializer = DocumentoSerializerIEEE(data=doc)
        	serializer.save(doc)
