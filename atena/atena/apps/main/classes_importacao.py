# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from urllib.parse import urlencode
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bsoup

class IEEE_Xplore_Searcher():
    apikey = '8m22c725rj99bvxq6pftexqk'
    address = 'http://ieeexploreapi.ieee.org/api/v1/search/articles?'

    def __init__(self, queryterms: list = None, apikey: str = None, address: str = None):
        self.articles_found = []
        if queryterms:
            self.queryterms = queryterms
        if apikey:
            self.apikey = apikey
        if address:
            self.address = address


    def search(self, queryterms: list=None, search_type: str="meta_data",
                start_year: int = None, end_year: int = None,content_type: str = None,
                start_record: int = 1, sort_field: str = None, sort_order: int = None,
                max_records: int = 200, article_title: str = None, author: str = None
        ):
        """
        @param queryterms: list of lists. Terms within the same list are
            separated by an OR. Lists are separated by an AND
        @param search_type: meta_data or querytext.
            meta_data: This field enables a free-text search of all
                configured metadata fields and the abstract. Accepts
                complex queries involving field names and  boolean
                operators.
            querytext: This field enables a free-text search of all
                configured metadata fields, abstract and document text.
                Accepts complex queries involving field names and boolean
                operators.
        @param start_year: Start value of Publication Year to restrict results by.
        @param end_year: End value of Publication Year to restrict results by.
        @param content_type: Note: these are case sensitive and must be spelled as
            presented here to get a result: Journals, Conference, Early Access,
            Standards, Books, Courses
        @param start_record: Sequence number of first record to fetch. Default: 1
        @param sort_field: Field name on which to sort. Choose from: article_number
            article_title, author, publication_title, publication_year
        @param sort_order: asc (for ascending sort) or desc (for descending sort)
        @param max_records: The number of records to fetch. Maximum: 200
        @param article_title: Title of an individual document (journal article,
            conference paper, standard, eBook chapter, or course).
        @param author: An author's name. Searches both first name and last name

        @return  the data fields returned by the search are described by the
            following link https://developer.ieee.org/docs/read/Metadata_API_responses
        """

        if not queryterms:
            queryterms = self.queryterms

        formated_query = "("
        for index_group, group in enumerate(queryterms):
            if index_group > 0:
                formated_query += '%20AND%20('
                #         else:
                # #             formated_query += '('
            for index_term, term in enumerate(group):
                if index_term > 0:
                    formated_query += '%20OR%20'
                if ' ' in term:
                    formated_query += '('
                formated_query += term.replace(' ', "%20")
                if ' ' in term:
                    formated_query += ')'

                if (index_term + 1) == len(group):
                    formated_query += ')'

        url = self.address + 'apikey=' + self.apikey
        if search_type == "meta_data":
            url += '&meta_data=' + formated_query
        elif search_type == "querytext":
            url += '&querytext=' + formated_query

        if start_year:
            url += '&start_year=' + str(start_year)
        if end_year:
            url += '&end_year=' + str(end_year)
        if content_type:
            url += '&content_type=' + content_type
        if start_record:
            url += '&start_record=' + str(start_record)
        if sort_field:
            url += '&sort_field=' + sort_field
        if sort_order:
            url += '&sort_order=' + sort_order
        if max_records:
            url += '&max_records=' + str(max_records)
        if article_title:
            url += '&article_title=' + article_title
        if author:
            url += '&author=' + author

        r = requests.get(url)
        total_records = r.json().get('total_records')
        print(round((total_records / max_records) + 0.4999), " requests needed...")
        self.articles_found = requests.get(url).json().get('articles')
        print("a request completed...")
        while (start_record + max_records) < total_records:
            start_record += max_records
            url = url.replace('&start_record=' + str(start_record - max_records),
                              '&start_record=' + str(start_record))
            self.articles_found += requests.get(url).json().get('articles')
            print("a request completed...")

        while len(self.articles_found) < total_records:
            pass

        return self.articles_found


class NCBI_Searcher(metaclass=ABCMeta):
    """ 'Interface' que define a utilização da API das databases da NCBI.
    """

    search_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    meta_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
    fetch_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

    def search(self, queryterms: list = None, search_type: str = None,
               start_year: int = 1900, end_year: int = None,
               max_records: int = 20, start_record: int = 0,
               author: str = None):
        """
        Realiza uma pesquisa NCBI.

        @param queryterms: list of lists. Terms within the same list are
            separated by an OR. Lists are separated by an AND
        @param search_type: meta_data or querytext.
            meta_data: This field enables a free-text search of all
                configured metadata fields and the abstract.
            querytext: This field enables a free-text search of all
                fields.
        @param start_year: Start value of Publication Year to restrict results by.
        @param end_year: End value of Publication Year to restrict results by.
        @param max_records: The number of records to fetch.
        @param start_record: Sequence number of first record to fetch.
        @param author: An author's name. Searches both first name and last name

        @return: uma lista de títulos e IDs no formato [(title, id)]
        """

        term = self._search_term(queryterms, search_type=search_type)
        if author:
            term = "%s AND %s[Author]" % (term, author)

        fixed_payload = {"retmode": "json", "datetype": "pdat",
                         "db": self._db, "sort": self._sort_order}
        payload = {"term": term,
                   "retmax": max_records, "retstart": start_record,
                   "mindate": start_year, "maxdate": end_year or datetime.now().year}
        payload.update(fixed_payload)

        url = "%s?%s" % (self.search_url, urlencode(payload))

        response = requests.get(url).json()['esearchresult']

        print('QTD. resultados: %s' % response['count'])

        id_list = response['idlist']

        if id_list:
            return self._get_article_metadata(*id_list)
        return []

    def _search_term(self, queryterms: list, search_type: str = None):
        """Monta o termo de pesquisa completo para mandar para a API."""

        if search_type in ['querytext', None]:
            # Retorna simplesmente a busca concatenando com os OR's e AND's
            return "(%s)" % " AND ".join(["(%s)" % " OR ".join(orses) for orses in queryterms])
        elif search_type != 'meta_data':
            raise Exception('Tipo de pesquisa não faz sentido: %s\nTipos suportados:' % search_type)

        # Retorna concacentando com os OR'S e AND's, mas embutindo também os campos de pesquisa em cada termo
        queryterms = [[self._embutir_fields(orses) for orses in andes] for andes in queryterms]
        return "(%s)" % " AND ".join(["(%s)" % " OR ".join(orses) for orses in queryterms])

    def _embutir_fields(self, term: str):
        """Faz uma transformação, embutindo fields no termo de pesquisa.
        Isso é para poder realizar a pesquisa em apenas alguns campos ao invés de todos.

        Exemplo: sendo self.__fields = ['title', 'abstract'],
        a chamada
        `self._embutir_fields("machine learning")`
        Transforma:
            machine learning ---> (machine learning[title] OR machine learning[abstract])
        """

        return "(%s)" % " OR ".join(["%s[%s]" % (term, field) for field in self._fields])

    @abstractmethod
    def _get_article_metadata(self, *args):
        """Cada subclasse deverá implementar a função que pega o retorno da API e transforma numa lista de dicionários
        no formato do modelo Documento."""
        pass

    @property
    @abstractmethod
    def _fields(self):
        """Cada subclasse deverá definir quais serão os campos de pesquisa de cada termo.
        O retorno deverá ser uma lista de fields.
        Exemplo:
        return ['title', 'abstract']
        """
        pass

    @property
    @abstractmethod
    def _db(self):
        """Cada subclasse deverá definir o seu banco.
        Exemplo:
        return 'pmc'
        """
        pass

    @property
    @abstractmethod
    def _sort_order(self):
        """Cada classe deverá definir o parâmetro sort_order.
        Exemplo:
        return 'Journal'
        """
        pass

    @property
    @abstractmethod
    def _article_url(self):
        """Cada classe deverá definir a URL da página de um artigo."""
        pass


class PMC_Searcher(NCBI_Searcher):
    """Realiza pesquisas na base PMC."""

    @property
    def _fields(self):
        return ['Abstract', 'Body - Key Terms', 'MeSH Terms',
                'MeSH Major Topic', 'Methods - Key Terms']

    @property
    def _db(self):
        return 'pmc'

    @property
    def _sort_order(self):
        return 'relevance'

    @property
    def _article_url(self):
        return 'https://www.ncbi.nlm.nih.gov/pmc/articles/'

    def _get_article_metadata(self, *args):
        id_list = ','.join([str(x) for x in args])

        payload = {"id": id_list, "db": self._db, "retmode": "xml"}
        url = "%s?%s" % (self.fetch_url, urlencode(payload))
        print(url)

        soup = bsoup(requests.get(url).content, "xml")

        pmc_articles = soup.findAll('article')

        documentos = []
        append = documentos.append
        for p_art in pmc_articles:
            author_list = p_art.findAll("contrib", {"contrib-type": "author"})
            authors = ["%s %s" % (getattr(a, "given-names").text, a.surname.text) for a in author_list]
            keywords = [k.text for k in p_art.findAll("kwd")]
            pub_date = p_art.findAll("pub-date", {"pub-type": "epub"})[0]
            data_pub_string = "%s %s" % (pub_date.year.text, pub_date.month.text)
            pmc_id = soup.findAll("article-id", {"pub-id-type": 'pmc'})[0].text

            documento = {}
            documento['resumo'] = getattr(p_art.abstract, 'text', '')
            documento['html_url'] = "%s%s" % (self._article_urlrece, pmc_id)
            documento['autores'] = ",".join(authors)
            documento['doi'] = p_art.findAll("article-id", {"pub-id-type": "doi"})[0].text
            documento['palavras_chaves'] = ",".join(keywords)
            documento['data'] = datetime.strptime(data_pub_string, "%Y %m").date()
            documento['titulo'] = getattr(p_art, "article-title").text
            append(documento)

        return documentos


class PubMed_Searcher(NCBI_Searcher):
    """Realiza pesquisas na base PubMed."""

    @property
    def _fields(self):
        return ['Text Words']

    @property
    def _db(self):
        return 'pubmed'

    @property
    def _sort_order(self):
        return ''

    @property
    def _article_url(self):
        return "https://www.ncbi.nlm.nih.gov/pubmed/"

    def _get_article_metadata(self, *args):
        id_list = ','.join([str(x) for x in args])

        payload = {"id": id_list, "db": self._db, "retmode": "xml"}
        url = "%s?%s" % (self.fetch_url, urlencode(payload))

        soup = bsoup(requests.get(url).content, "xml")

        pubmed_articles = soup.findAll('PubmedArticle')

        documentos = []
        append = documentos.append
        for p_art in pubmed_articles:
            authors = ["%s %s" % (a.ForeName.text, a.LastName.text) for a in p_art.findAll("Author")]
            keywords = [k.text for k in p_art.findAll("Keyword")]
            data_pub_string = "%s %s" % (p_art.PubDate.Year.text, p_art.PubDate.Month.text)

            documento = {}
            documento['resumo'] = getattr(p_art.AbstractText, 'text', '')
            documento['html_url'] = "%s%s" % (self._article_url, p_art.PMID.text)
            documento['autores'] = ",".join(authors)
            documento['doi'] = p_art.findAll("ArticleId", {"IdType": "doi"})[0].text
            documento['palavras_chaves'] = ",".join(keywords)
            documento['data'] = datetime.strptime(data_pub_string, "%Y %b").date()
            documento['titulo'] = p_art.ArticleTitle.text
            append(documento)

        return documentos