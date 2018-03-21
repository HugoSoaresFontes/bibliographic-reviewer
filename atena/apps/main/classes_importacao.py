# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from urllib.parse import urlencode
import requests
from .utils import ThreadWithReturnValue
from datetime import datetime
from bs4 import BeautifulSoup as bsoup
from functools import reduce
import time
import xmltodict, json

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
    max_pagination = 20
    recursive = True

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

        fixed_payload = {"retmode": "json", "datetype": "pdat",
                         "db": self._db, "sort": self._sort_order}
        payload = {"term": term,
                   "retmax": max_records or '', "retstart": start_record or '',
                   "mindate": start_year or '', "maxdate": end_year or ''}
        payload.update(fixed_payload)
        payload.update(self.ncbi_register)
        url = search_url if search_url else "%s?%s" % (self.search_url, urlencode(payload))

        #         print("URL SEARCH: %s" % url)
        t_00 = time.time()
        response = requests.get(url).json()['esearchresult']
        print('{:15s}{:6.3f}'.format("response", time.time() - t_00))
        quantidade_artigos = int(response['count'])
        if self.recursive:
            print("Artigos encontrados: ", quantidade_artigos)
        # Se o usuário não limitou quantidade de resultados, então traz tudo
        max_records = max_records or quantidade_artigos

        retorno = []

        ###
        ### BLOCO FANTASMA
        ###
        # Se houver necessidade de paginação...
        #         if quantidade_artigos > self.max_pagination and max_records > self.max_pagination:
        #             # self.recursive só sera True se a chamada estiver sendo feita pelo usuário.
        #             # Isso serve para garantir que cada chamada da função self.search
        #             # neste bloco só acontecerá com um nível de recursividade.
        #             if self.recursive:
        #                 self.recursive = False

        #                 threads = []
        #                 payload.update({'retmax':self.max_pagination})
        #                 for i,x in enumerate(range(20, quantidade_artigos+1, self.max_pagination)):

        #                     payload.update({'retstart':x})
        #                     kwargs = {"search_url": "%s?%s" % (self.search_url, urlencode(payload))}

        #                     thread = ThreadWithReturnValue(target=self.search, kwargs=kwargs)
        #                     threads.append(thread)
        #                     thread.start()

        #                     if (i+1)%3==0:
        #                         print("sleeping")
        #                         time.sleep(2)

        #                 for thread in threads:
        #                     lista = thread.join()
        #                     print("thread fetching ",len(lista))
        #                     retorno.extend(lista)

        #                 self.recursive = True

        ###
        ### FIM BLOCO FANTASMA
        ###

        id_list = response['idlist']

        if id_list:
            lista = self._get_article_metadata(*id_list)
            retorno.extend(lista)
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

    @staticmethod
    def deepgetter(obj, attrs, default=None):
        """Faz uma chamada sucessiva da função getattr, para ir pegando os atributos
        de um objeto.
        Exemplo:
        deepgetter(Cidade, 'regiao.pais') é equivalente a fazer Cidade.regiao.pais
        """
        getter = lambda x, y: getattr(x, y, default)
        return reduce(getter, attrs.split('.'), obj)

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

    @staticmethod
    def _get_data(p_art):
        """Vasculha o XML (um <PubmedArticle>) para encontrar a data de publicação
        Se for encontrada uma data válida, retorna um datetime.
        Se não, retorna uma string, que espera-se que contenha uma informação de data"""

        try:
            pub_date = p_art.findAll("pub-date", {"pub-type": "epub"})[0]
        except:
            pub_date = p_art.findAll("pub-date", {"pub-type": "ppub"})[0]

        data_pub_string = "%s %s" % (
        pub_date.year.text, NCBI_Searcher.deepgetter(pub_date, 'month.text', default='Jan'))

        try:
            data = datetime.strptime(data_pub_string, "%Y %m").date()
        except:
            try:
                data = datetime.strptime(data_pub_string, "%Y %b").date()
            except:
                data = data_pub_string

        return data

    @staticmethod
    def _get_unique_id(p_art):
        """Vascula o XML (um <PubmedArticle>) para encontrar o ID único do artigo.
        Se nao tiver DOI presente no XML, coloca o ID que tiver (esperado que seja o PubMed ID)"""

        try:
            unique_id = p_art.findAll("article-id", {"pub-id-type": "doi"})[0].text
        except:
            unique_id = p_art.findAll("article-id")[0]
            unique_id = "%s%s" % (unique_id['pub-id-type'], unique_id.text)

        return unique_id

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
        articles = d['pmc-articleset']['article']
        print('{:15s}{:6.3f}'.format("parse", time.time() - t_02))

        documentos = []
        append = documentos.append

        t_04 = time.time()
        debug = False
        for article in articles:
            ### TITULO
            # try:
            title = article['front']['article-meta']['title-group']['article-title']
            # except Exception as e:
            #     title = ''
            #     print(e.__class__.__name__, e)
            #     if debug:
            #         ipdb.set_trace()

            ### AUTORES
            try:
                authors = []
                for contrib in article['front']['article-meta']['contrib-group']['contrib']:
                    try:
                        authors.append("%s %s" % (contrib['name']['given-names'], contrib['name']['surname']))
                    except:
                        pass
            except Exception as e:
                authors = []
                print(e.__class__.__name__, e)
            #     if debug:
            #         ipdb.set_trace()

            ### PALAVRAS CHAVE
            try:
                palavras_chave = [k if type(k) == str else k['#text'] for k in
                                  article['front']['article-meta']['kwd-group']['kwd']]
            except Exception as e:
                palavras_chave = []
                print(e.__class__.__name__, e)

            ### DOI / IDs
            pmc_id = [id['#text'] for id in article['front']['article-meta']['article-id'] if id['@pub-id-type'] == 'pmc'][-1] or ''
            try:
                doi = \
                [id['#text'] for id in article['front']['article-meta']['article-id'] if id['@pub-id-type'] == 'doi'][
                    -1] or ''
            except Exception as e:
                doi = ''
                print(e.__class__.__name__, e)
            #     if debug:
            #         ipdb.set_trace()

            ### Abstract
            try:
                abstract = article['front']['article-meta']['abstract']
                if type(abstract) == dict:
                    try:
                        resumo = abstract['p']['#text']
                    except:
                        resumo = ''
                elif type(abstract) == list:
                    for ab in abstract:
                        try:
                            ab['@abstract-type']
                        except:
                            continue

                        if ab['@abstract-type'] == 'author-highlights':

                            if type(ab['p']) == dict:
                                resumo = ab['p']['#text']
                            elif type(ab['p']) == list:
                                resumo = ''
                                for p in ab['p']:
                                    try:
                                        p['#text']
                                    except:
                                        continue
                                    resumo = "%s\n%s" % (resumo, p['#text'])
                else:
                    resumo = ''
            except Exception as e:
                resumo = ''
                print(e.__class__.__name__, e)
            #     if debug:
            #         ipdb.set_trace()

            ### Fim da grosseria

            documento = {}
            documento['resumo'] = resumo
            print("%s%s" % (self._article_url, pmc_id))
            documento['html_url'] = "%s%s" % (self._article_url, pmc_id)
            documento['autores'] = ",".join(authors)
            documento['doi'] = doi
            documento['palavras_chaves'] = ",".join(palavras_chave)
            documento['titulo'] = title

            append(documento)

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

    @staticmethod
    def _get_data(p_art):
        """Vasculha o XML (um <PubmedArticle>) para encontrar a data de publicação
        Se for encontrada uma data válida, retorna um datetime.
        Se não, retorna uma string, que espera-se que contenha uma informação de data"""

        if hasattr(p_art.PubDate.Year, "text"):
            ano = p_art.PubDate.Year.text
        elif hasattr(p_art.PubDate.MedlineDate, "text"):
            ano = p_art.PubDate.MedlineDate.text[:8]

        try:
            data_pub_string = "%s %s" % (ano, NCBI_Searcher.deepgetter(p_art, 'PubDate.Month.text', default='Jan'))
            data = datetime.strptime(data_pub_string, "%Y %b").date()
        except:
            try:
                data_pub_string = "%s %s" % (ano, NCBI_Searcher.deepgetter(p_art, 'PubDate.Month.text', default='Jan'))
                data = datetime.strptime(data_pub_string, "%Y %m").date()
            except:
                data = str(p_art.PubDate.text)

        return data

    @staticmethod
    def _get_unique_id(p_art):
        """Vascula o XML (um <PubmedArticle>) para encontrar o ID único do artigo.
        Se nao tiver DOI presente no XML, coloca o ID que tiver (esperado que seja o PubMed ID)"""

        try:
            unique_id = p_art.findAll("ArticleId", {"IdType": "doi"})[0].text
        except:
            unique_id = p_art.findAll("ArticleId")[0]
            unique_id = "%s%s" % (unique_id['IdType'], unique_id.text)

        return unique_id

    def _get_article_metadata(self, *args):
        id_list = ','.join([str(x) for x in args])

        payload = {"id": id_list, "db": self._db, "retmode": "xml"}
        url = "%s?%s" % (self.fetch_url, urlencode(payload))

        print("URL META: %s" % url)

        soup = bsoup(requests.get(url).content, "xml")

        pubmed_articles = soup.findAll('PubmedArticle')

        documentos = []
        append = documentos.append

        for p_art in pubmed_articles:
            authors = ["%s %s" % (a.ForeName.text, a.LastName.text) for a in p_art.findAll("Author")]
            keywords = [k.text for k in p_art.findAll("Keyword")]

            documento = {}
            documento['resumo'] = getattr(p_art.AbstractText, 'text', ' - ')
            documento['html_url'] = "%s%s" % (self._article_url, p_art.PMID.text)
            documento['autores'] = ",".join(authors)
            documento['doi'] = self._get_unique_id(p_art)
            documento['palavras_chaves'] = ",".join(keywords)
            documento['titulo'] = p_art.ArticleTitle.text
            data = self._get_data(p_art)
            if type(data) == str:
                documento['resumo'] = "%s\n%s" % (data, documento['resumo'])
            else:
                documento['data'] = self._get_data(p_art)

            append(documento)

        return documentos