import pytz
from rest_framework import (generics, permissions, response, status)
from django.utils.timezone import localtime
from BNDESIntegration import serializers
from .models import BNDESTransaction, Company,  ArchiveBNDESTransaction
import requests
from datetime import datetime
from connect_api import settings
from django.core.exceptions import ObjectDoesNotExist


class BNDES:

    response = None
    url = settings.BNDES_URL

    @staticmethod
    def get_bndes_data(request, specific_param):
        """Static Method for get all information avaiable on the requested
        data from defined param.

        Args:
            request (HTTP Request): HTTP Request.
            specific_param (string): CPF or CNPJ

        Returns:
            response (dict) : BNDES requested response

        """

        params = specific_param
        print(params)
        client_id = BNDES.post_client_identifiers(params)
        url = BNDES.url + '/%s' % (client_id.cnpj)

        verified_url = BNDES.validate_expiration_date(url, params)
        if not verified_url:
            client_id = BNDES.post_client_identifiers(params)
            verified_url = url

        # If exists on database, get from there! If not request
        transaction_exxists = BNDES.get_database_info(client_id)

        if transaction_exxists == None:
            print('on database: False')
            BNDES.get_request(verified_url)
            if BNDES.response:
                BNDES.store_bndes_response(BNDES.response, client_id)

        response = None
        if BNDES.response:
            response = BNDES.response
            BNDES.response = None
        elif transaction_exxists:
            print('on database: True')
            response = transaction_exxists.logs

        return response

    @classmethod
    def validate_expiration_date(cls, url, params):
        """METHOD for delete or continue request.
        When expiration_date is True, need to remove all operation about specif client,
        else continue request normally

        Args:
            url (string): url to request data
        """
        client_verify = Company.objects.get(
            cnpj=params,
        )
        expiration_date = localtime(client_verify.validity_day)

        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        print("out of expiry date: ", expiration_date < today)
        if expiration_date < today:
            BNDES.store_bndes_archive_data(params, client_verify)
        else:
            return url

    @classmethod
    def post_client_identifiers(cls, params):
        """METHOD for save on database as Primary key
        the receive params

        Args:
            params (string): CPF or CNPJ
        """
        client, obj = Company.objects.filter(cnpj=params).get_or_create(
            cnpj=params
        )
        print('Who: ', client)
        print('Needs Create: ', obj)
        if obj:
            client.save()
        return client

    @classmethod
    def get_request(cls, url):
        """METHOD to send request to given url
        and store in BNDES.response global variable

        Args:
            url (str) : BNDES endpoint url.
        """

        response_get = requests.get(url).json()

        if (
            len(response_get.get("operacoes")) != 0 or
            len(response_get.get("desembolsos")) != 0 or
            len(response_get.get("carteira")) != 0
        ):
            BNDES.response = response_get

    @classmethod
    def store_bndes_response(cls, response, client):
        """Method for storing BNDES response("operacoes") in OPERACOES model

        Args:
            response(dict) : BNDES response, 
        """

        serializer_data = {}
        serializer_data["client"] = client.id
        serializer_data["logs"] = response

        serializer = serializers.BNDESTransactionSerializers(
            data=serializer_data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

    @classmethod
    def store_bndes_archive_data(cls, client, params):
        """Method for storing BNDES response("operacoes") in OPERACOES model

        Args:
            response(dict) : BNDES response, 
        """
        old_data = BNDESTransaction.objects.get(client=client)

        serializer_data = {}
        serializer_data["client"] = client
        serializer_data["logs"] = old_data.logs

        serializer = serializers.ArchiveBNDESTransactionSerializers(
            data=serializer_data
        )
        print("objeto do lixo criado")
        serializer.is_valid()
        serializer.save()
        params.delete()
        return False

    @classmethod
    def store_bndes_response_oper(cls,):
        pass

    @classmethod
    def get_database_info(cls, client):
        """ METHOD to get database info, before request on webpage
        ARGS:
            client (query): query from tb_company
        """
        try:
            query_transactions = BNDESTransaction.objects.get(client=client)
            return query_transactions

        except ObjectDoesNotExist:
            return None
