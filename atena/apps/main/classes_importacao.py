# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import requests
from elsapy.elsclient import ElsClient
from .utils import dive, inclusive_range, get_all_text
from urllib.parse import urlencode, quote_plus
from datetime import datetime
import re
import time
import xmltodict, json
import ipdb

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
                start_year: int = None, end_year: int = None,content_type: str = 'Journals',
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


class ElsevierSearcher:
    __base_url = u'https://api.elsevier.com/content/search/'
    __api_key = u'e7882eed968063f188d6c53a919528a7'

    def __init__(self, index: str, apikey: str = __api_key):
        self.articles_found = []
        self.apikey = apikey
        self.index = index
        self.els_client = ElsClient(self.apikey)
        self._uri = self.__base_url + index + '?'

    def search(self, queryterms: list = None,
               start_year: int = None, end_year: int = None,
               content_type: str = 'journals', start_record: int = None,
               sort_field: str = None, sort_order: int = None,
               max_records: int = None, article_title: str = None, author: list = None, journal: list = None):
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

        @return  the data fields returned by the search are described by the
            following link https://developer.ieee.org/docs/read/Metadata_API_responses
        """

        formated_query = ''
        if self.index == 'scopus':
            formated_query = "TITLE-ABS-KEY(("
        if self.index == 'scidir':
            formated_query = "tak(("
        for index_group, group in enumerate(queryterms):
            if index_group > 0:
                formated_query += ' AND ('
            #         else:
            # #             formated_query += '('
            for index_term, term in enumerate(group):
                if index_term > 0:
                    formated_query += ' OR '
                formated_query += f'"{term}"'

                if (index_term + 1) == len(group):
                    formated_query += ')'
        formated_query += ')'

        if author:
            str_author = ' AND '.join([f'"{x}"' for x in author])
            if self.index == 'scopus':
                formated_query += f' AND AUTHOR-NAME({str_author})'
            if self.index == 'scidir':
                formated_query += f' AND aut({str_author})'
        if article_title:
            if self.index == 'scopus':
                formated_query += f' AND TITLE("{article_title}")'
            if self.index == 'scidir':
                formated_query += f' AND ttl("{article_title}")'
        if journal:
            str_journal = ' AND '.join([f'"{x}"' for x in journal])
            if self.index == 'scopus':
                formated_query += f' AND SRCTITLE({str_journal})'
            if self.index == 'scidir':
                formated_query += f' AND src({str_journal})'

        query_params = dict()

        print(formated_query)
        query_params['query'] = formated_query
        #         query_params['view'] = 'STANDARD'

        if start_year:
            start_year = str(start_year)
            date = start_year
            if end_year:
                end_year = str(end_year)
                date += f'-{end_year}'
            query_params['date'] = date
        if content_type:
            query_params['content'] = content_type
        if start_record:
            query_params['start'] = start_record
        if max_records:
            query_params['count'] = max_records

        get_all = True

        url = self._uri + urlencode(query_params, quote_via=quote_plus)
        print(url)

        self._api_response = self.els_client.exec_request(url)
        self._tot_num_res = int(self._api_response['search-results']['opensearch:totalResults'])
        self.results = self._api_response['search-results']['entry']
        print("a request completed...")
        if get_all is True:
            while (len(self.results) < self._tot_num_res) and (len(self.results) < 5000):
                for e in self._api_response['search-results']['link']:
                    if e['@ref'] == 'next':
                        next_url = e['@href']
                self._api_response = self.els_client.exec_request(next_url)
                self.results += self._api_response['search-results']['entry']
                print("a request completed...")

        return self.results


class NCBI_Searcher(metaclass=ABCMeta):
    """ 'Interface' que define a utilização da API das databases da NCBI.
    """

    search_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    meta_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
    fetch_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    ncbi_register = {"tool": "Atena", "email": "ddddiegolima@gmail.com"}
    recursive = True
    request_uri_limit = 100

    def search(self, queryterms: list = None, search_type: str = None,
               start_year: int = None, end_year: int = None,
               max_records: int = None, start_record: int = None,
               author: str = None, journal: str = None, search_url: str = None):
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
            Accepts a list of author names too.
        @param journal: An author's name. Accepts a list of journals too.
        @param search_url: Optionally you can directly specify the URL to
            query from. Setting this parameter will ignore the other parameters.
        @return: a dictionaries list whose keys are compatible with Documento model.
        """

        term = self._search_term(queryterms, search_type=search_type)
        if author:
            author = [author] if type(author) == str else author
            author = ['%s[Author]' % a for a in author]
            term = "%s AND (%s)" % (term, " OR ".join(author))

        if journal:
            journal = [journal] if type(journal) == str else journal
            journal = ['"%s"[Journal]' % j for j in journal]
            term = "%s AND (%s)" % (term, " OR ".join(journal))

        print(term)

        if max_records and max_records > self.request_uri_limit:
            retmax = self.request_uri_limit
        else:
            retmax = max_records

        fixed_payload = {"retmode": "json", "datetype": "pdat",
                         "db": self._db, "sort": self._sort_order}
        payload = {"term": term,
                   "retmax": retmax or '', "retstart": start_record or '',
                   "mindate": start_year or '', "maxdate": end_year or ''}
        payload.update(fixed_payload)
        payload.update(self.ncbi_register)
        url = search_url if search_url else "%s?%s" % (self.search_url, urlencode(payload))

        print("URL SEARCH: %s" % url)
        t_00 = time.time()
        response = requests.get(url).json()['esearchresult']
        print('{:15s}{:6.3f}'.format("response", time.time() - t_00))
        quantidade_artigos = int(response['count'])
        if self.recursive:
            print("Artigos encontrados: ", quantidade_artigos)
        # Se o usuário não limitou quantidade de resultados, então traz tudo
        max_records = max_records or quantidade_artigos

        retorno = []
        id_list = response['idlist']

        if id_list:
            lista = self._get_article_metadata(*id_list)
            retorno.extend(lista)

        if max_records > self.request_uri_limit and self.recursive:
            # self.recursive só sera True se a chamada estiver sendo feita pelo usuário.
            # Isso serve para garantir que cada chamada da função self.search
            # neste bloco não provocará recursividade.
            self.recursive = False

            for retstart, retmax in inclusive_range(len(retorno), max_records, self.request_uri_limit):
                payload.update({'retstart': retstart})
                payload.update({'retmax': retmax})
                kwargs = {"search_url": "%s?%s" % (self.search_url, urlencode(payload))}

                lista = self.search(**kwargs)
                retorno.extend(lista)

            self.recursive = True

        return retorno

    def _search_term(self, queryterms: list, search_type: str = None):
        """Monta o termo de pesquisa completo para mandar para a API."""

        if type(queryterms) != list:
            return

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
        payload.update(self.ncbi_register)
        url = "%s?%s" % (self.fetch_url, urlencode(payload))
        print("URL META: %s" % url)

        t_05 = time.time()
        r = requests.get(url)
        print('{:15s}{:6.3f}'.format("response_M", time.time() - t_05))

        t_02 = time.time()
        # Pegar o XML, e transformar num dicionário
        d = json.loads(json.dumps(xmltodict.parse(r.content)))
        artigos = d['pmc-articleset']['article']
        print('{:15s}{:6.3f}'.format("parse", time.time() - t_02))

        documentos = []
        append = documentos.append

        t_04 = time.time()
        debug = False

        for artigo in artigos:
            diver = lambda route: dive(artigo, route)
            doc = {}

            ### TITULO
            try:
                titulo = diver('front.article-meta.title-group.article-title')
                titulo = get_all_text(titulo)
                doc['titulo'] = " ".join(titulo)
            except Exception as e:
                print('erro:', 'titulo')
                print(repr(e))
                if debug:
                    ipdb.set_trace()

            ### RESUMO / ABSTRACT
            try:
                resumo = diver('front.article-meta.abstract')
                resumo = get_all_text(resumo, ['sec'])
                doc['resumo'] = "\n".join(resumo)
            except Exception as e:
                print('erro:', 'resumo')
                print(repr(e))
                if debug:
                    ipdb.set_trace()

            ### PALAVRAS-CHAVE
            try:
                keywords = diver('front.article-meta.kwd-group')
                keywords = get_all_text(keywords, ['kwd'])
                doc['palavras_chave'] = ",".join(keywords)
            except Exception as e:
                print('erro:', 'keywords')
                print(repr(e))
                if debug:
                    ipdb.set_trace()

            ### AUTORES
            try:
                authors = diver('front.article-meta.contrib-group')
                if isinstance(authors, dict):
                    authors = authors['contrib']

                elif isinstance(authors, list):
                    authors = authors[0]['contrib']

                if isinstance(authors, dict):
                    name = authors.get('name', None)
                    if name:
                        authors = "%s %s" % (name['given-names'], name['surname'])
                elif isinstance(authors, list):
                    list_ = []
                    for a in authors:
                        name = a.get('name', None)
                        if name:
                            list_.append("%s %s" % (name['given-names'], name['surname']))
                    authors = ",".join(list_)

                doc['autores'] = authors
            except Exception as e:
                print('erro:', 'authors')
                print(repr(e))
                if debug:
                    ipdb.set_trace()

            article_ids = diver('front.article-meta.article-id')
            ### HTML_URL
            try:
                pmc_id = [a for a in article_ids if a["@pub-id-type"] == 'pmc'][0]['#text']

                doc['html_url'] = "%s%s" % (self._article_url, pmc_id)
            except Exception as e:
                print('erro:', 'html_url')
                print(repr(e))
                if debug:
                    ipdb.set_trace()

            ### DOI
            try:
                doi = [a for a in article_ids if a["@pub-id-type"] == 'doi'][0]['#text']

                doc['doi'] = doi
            except Exception as e:
                print('erro:', 'doi')
                print(repr(e))
                if debug:
                    ipdb.set_trace()

            ### DATA
            try:

                data = diver('front.article-meta.pub-date')
                if isinstance(data, dict):
                    data = [data]
                data = data[0]
                data = "%s %s" % (data['year'], data.get('month', '01'))
                doc['data'] = datetime.strptime(data, "%Y %m").date()
            except Exception as e:
                print('erro:', 'data')
                print(repr(e))
                if debug:
                    ipdb.set_trace()

            append(doc)

        print('{:15s}{:6.3f}'.format("fetch", time.time() - t_04))

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
        payload.update(self.ncbi_register)
        url = "%s?%s" % (self.fetch_url, urlencode(payload))

        print("URL META: %s" % url)

        t_05 = time.time()
        r = requests.get(url)
        print('{:15s}{:6.3f}'.format("response_M", time.time() - t_05))

        t_02 = time.time()
        # Pegar o XML, e transformar num dicionário
        d = json.loads(json.dumps(xmltodict.parse(r.content)))
        artigos = d['PubmedArticleSet']['PubmedArticle']
        if isinstance(artigos, dict):
            # No caso de vir somente um artigo no resultado
            artigos = [artigos]
        print('{:15s}{:6.3f}'.format("parse", time.time() - t_02))

        documentos = []
        append = documentos.append

        t_04 = time.time()
        debug = False

        for artigo in artigos:
            diver = lambda route: dive(artigo, route)
            doc = {}

            ### TITULO
            titulo = diver('MedlineCitation.Article.ArticleTitle')
            titulo = get_all_text(titulo)
            doc['titulo'] = " ".join(titulo)

            ### RESUMO / ABSTRACT
            try:
                resumo = diver('MedlineCitation.Article.Abstract.AbstractText')
                resumo = get_all_text(resumo)
                doc['resumo'] = "\n".join(resumo)
            except:
                print("resumo")
                if debug:
                    ipdb.set_trace()

            ### PALAVRAS-CHAVE
            try:
                keywords = diver('MedlineCitation.KeywordList.Keyword')
                keywords = get_all_text(keywords)
                doc['palavras_chave'] = ",".join(keywords)
            except:
                print("keywords")
                if debug:
                    ipdb.set_trace()

            ### AUTORES
            authors = diver('MedlineCitation.Article.AuthorList.Author')
            try:
                if isinstance(authors, list):
                    authors = ",".join(
                        ["%s %s %s" % (a.get('ForeName', ''), a.get('LastName', ''), a.get('CollectiveName', '')) for a
                         in authors])
                elif isinstance(authors, dict):
                    authors = "%s %s %s" % (
                    authors.get('ForeName', ''), authors.get('LastName', ''), authors.get('CollectiveName', ''))
                doc['autores'] = authors
            except:
                print("authors")
                if debug:
                    ipdb.set_trace()

            ### PMID (URL HTML)
            try:
                html_url = diver('MedlineCitation.PMID.#text')
                doc['html_url'] = "%s%s" % (self._article_url, html_url)
            except:
                print('html_url')
                if debug:
                    ipdb.set_trace()

            ### DOI
            try:
                doi = diver('PubmedData.ArticleIdList.ArticleId')
                doi = [d['#text'] for d in doi if d['@IdType'] == 'doi']
                if not doi:
                    doi = ''
                else:
                    doi = doi[0]
                doc['doi'] = doi
            except:
                print('doi')
                if debug:
                    ipdb.set_trace()

            ### DATA
            try:
                data = diver(['MedlineCitation.Article.ArticleDate', 'PubmedData.History.PubMedPubDate'])
                if isinstance(data, dict):
                    data = "%s %s" % (data['Year'], data.get('Month', '01'))
                if isinstance(data, list):
                    data = "%s %s" % (data[0]['Year'], data[0].get('Month', '01'))
                doc['data'] = datetime.strptime(data, "%Y %m").date()
            except:
                print('data')
                if debug:
                    ipdb.set_trace()

            append(doc)

        print('{:15s}{:6.3f}'.format("fetch", time.time() - t_04))

        return documentos


class Springer_Searcher():
    api_key = 'f1333dfd6f52767d0a77099010fbefbc'
    address = 'http://api.springer.com/meta/v1/json?'

    def __init__(self, queryterms: list = None, api_key: str = None, address: str = None):
        self.articles_found = []
        if queryterms:
            self.queryterms = queryterms
        if api_key:
            self.api_key = api_key
        if address:
            self.address = address

    def search(self, queryterms: list = None, max_records: int = 2500, start_record: int = 1, type: str = 'Journal', year: int = None, end_year: int = None):
        """
        @param queryterms: list of lists. Terms within the same list are
            separated by an OR. Lists are separated by an AND
        @param max_records: Number of results to return in this request.
        @param start_record: Return results starting at the number specified.
        @param year: limit to articles/chapters published from a particular year.
                     If left blank will serach all year
        @param end_year: limit to articles/chapters published from a @year to actual @end_year.
                     If left blank will serach all year
        @param type: limit to either Book or Journal content {Book, Journal}
        """

        if not queryterms:
            queryterms = self.queryterms

        formated_query = " AND ".join(["(%s)" % " OR ".join(term) for term in queryterms])

        url = self.address + "q=" + formated_query

        if type:
            url += ' AND type:'+type

        if year:
            url += ' AND year:' + str(year)
            if max_records:
                url += '&p=' + str(max_records)
            if start_record:
                url += '&s=' + str(start_record)

            url += '&api_key=' + self.api_key

            r = requests.get(url)

            lst = re.findall("'\S+'", str(r.json().get('result')))
            index_of_total = lst.index("'total'")

            if end_year and end_year > year:
                last_year = end_year
            else:
                last_year = year

            while year <= last_year:
                r = requests.get(url)

                lst = re.findall("'\S+'", str(r.json().get('result')))
                index_of_total = lst.index("'total'")
                total_records = int(lst[index_of_total + 1][1:-1])

                print("Requisition: ")
                print("\n", r.url, "\n")
                print("Articles found in ", year, ": ", total_records)
                print(round((total_records / max_records) + 0.4999), " requests needed...")
                self.articles_found += r.json().get('records')
                print(year, " request completed...")
                while (start_record + max_records) < total_records:
                    url = url.replace('&s=' + str(start_record),
                                      '&s=' + str(start_record + max_records))
                    r = requests.get(url)
                    self.articles_found += r.json().get('records')
                    start_record += max_records
                url = url.replace('year:' + str(year), 'year:' + str(year + 1))
                year += 1

            return self.articles_found

        if max_records:
            url += '&p=' + str(max_records)
        if start_record:
            url += '&s=' + str(start_record)

        url += '&api_key=' + self.api_key

        r = requests.get(url)

        lst = re.findall("'\S+'", str(r.json().get('result')))
        index_of_total = lst.index("'total'")
        total_records = int(lst[index_of_total + 1][1:-1])

        print("Requisição: ")
        print("\n", r.url, "\n")
        print(round((total_records / max_records) + 0.4999), " requests needed...")
        self.articles_found = r.json().get('records')
        print("a request completed...")
        while (start_record + max_records) < total_records:
            url = url.replace('&s=' + str(start_record),
                              '&s=' + str(start_record + max_records))
            r = requests.get(url)
            self.articles_found += r.json().get('records')
            start_record += max_records
            print("a request completed...")

        return self.articles_found