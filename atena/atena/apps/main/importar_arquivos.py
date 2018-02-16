# -*- coding: utf-8 -*-
from .classes_importacao import IEEE_Xplore_Searcher
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

def importar_arquivos(revisao, base):
    if base == "IEEE Xplore":
        ieee_searcher = IEEE_Xplore_Searcher()
        documentos = ieee_searcher.search(queryterms=queryterms,
                                        start_year=1975, content_type="Journals",
                                        search_type="meta_data", max_records=200)

