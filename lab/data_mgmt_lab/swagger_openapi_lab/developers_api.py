# coding: utf-8

"""
    Simple Inventory API

    This is a simple API  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: you@your-company.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from swagger_client.api_client import ApiClient


class DevelopersApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def search_inventory(self, **kwargs):  # noqa: E501
        """searches inventory  # noqa: E501

        By passing in the appropriate options, you can search for available inventory in the system   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_inventory(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str search_string: pass an optional search string for looking up inventory
        :param int skip: number of records to skip for pagination
        :param int limit: maximum number of records to return
        :return: list[InventoryItem]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.search_inventory_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.search_inventory_with_http_info(**kwargs)  # noqa: E501
            return data

    def search_inventory_with_http_info(self, **kwargs):  # noqa: E501
        """searches inventory  # noqa: E501

        By passing in the appropriate options, you can search for available inventory in the system   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_inventory_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str search_string: pass an optional search string for looking up inventory
        :param int skip: number of records to skip for pagination
        :param int limit: maximum number of records to return
        :return: list[InventoryItem]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['search_string', 'skip', 'limit']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method search_inventory" % key
                )
            params[key] = val
        del params['kwargs']

        if 'skip' in params and params['skip'] < 0:  # noqa: E501
            raise ValueError("Invalid value for parameter `skip` when calling `search_inventory`, must be a value greater than or equal to `0`")  # noqa: E501
        if 'limit' in params and params['limit'] > 50:  # noqa: E501
            raise ValueError("Invalid value for parameter `limit` when calling `search_inventory`, must be a value less than or equal to `50`")  # noqa: E501
        if 'limit' in params and params['limit'] < 0:  # noqa: E501
            raise ValueError("Invalid value for parameter `limit` when calling `search_inventory`, must be a value greater than or equal to `0`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'search_string' in params:
            query_params.append(('searchString', params['search_string']))  # noqa: E501
        if 'skip' in params:
            query_params.append(('skip', params['skip']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/inventory', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[InventoryItem]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
