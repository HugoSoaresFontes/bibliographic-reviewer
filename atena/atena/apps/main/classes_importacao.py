# -*- coding: utf-8 -*-
import requests
from elsapy.elsclient import ElsClient
from urllib.parse import urlencode, quote_plus

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
        self.els_client = ElsClient(self.apikey)
        self._uri = self.__base_url + index + '?'

    def search(self, queryterms: list = None,
               start_year: int = None, end_year: int = None,
               content_type: str = 'journals', start_record: int = None,
               sort_field: str = None, sort_order: int = None,
               max_records: int = None, article_title: str = None, author: list = None):
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

        if not queryterms:
            queryterms = self.queryterms

        formated_query = "("
        for index_group, group in enumerate(queryterms):
            if index_group > 0:
                formated_query += ' AND ('
            #         else:
            # #             formated_query += '('
            for index_term, term in enumerate(group):
                if index_term > 0:
                    formated_query += ' OR '
                if ' ' in term:
                    formated_query += '('
                formated_query += f'"{term}"'
                if ' ' in term:
                    formated_query += ')'

                if (index_term + 1) == len(group):
                    formated_query += ')'
        if author:
            str_author = ' AND '.join([f'"{x}"' for x in author])
            formated_query += f' AND aut({str_author})'
        if article_title:
            formated_query += f' AND ttl({article_title})'

        query_params = dict()

        query_params['query'] = formated_query
        #         query_params['view'] = 'STANDARD'

        if start_year:
            date = start_year
            if end_year:
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