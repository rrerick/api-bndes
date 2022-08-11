import pytz
from rest_framework import (generics, permissions, response, status)
from django.utils.timezone import localtime
from BNDESIntegration import serializers
from .models import BNDESOperacoes, Empresa,  ArchiveBNDESOperacoes
import requests
from datetime import datetime
from connect_api import settings


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
        url = BNDES.url + '/%s' % (client_id.cnpj_id)
        verified_url = BNDES.validate_expiration_date(url, params)
        if not verified_url:
            client_id = BNDES.post_client_identifiers(params)
            verified_url = url

        # hora de requisitar ao BNDES
        if verified_url:
            BNDES.get_request(verified_url)
            if BNDES.response:
                BNDES.store_bndes_response(BNDES.response, client_id)

        response = None
        if BNDES.response:
            response = BNDES.response
            BNDES.response = None

        return response

    @classmethod
    def validate_expiration_date(cls, url, params):
        """METHOD for delete or continue request.
        When expiration_date is True, need to remove all operation about specif client,
        else continue request normally

        Args:
            url (string): url to request data
        """
        client_verify = Empresa.objects.get(
            cnpj_id=params,
        )
        expiration_date = localtime(client_verify.validity_day)

        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        print("On validity: ", expiration_date < today)
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

        client, obj = Empresa.objects.filter(cnpj_id=params).get_or_create(
            cnpj_id=params
        )

        if obj == False:
            client.save()

        return client

    @classmethod
    def get_request(cls, url):
        """METHOD to send request to given url
        and store in BNDES.response global variable

        Args:
            url (str) : BNDES endpoint url.
        """

        response = requests.get(url).json()
        obje = response['operacoes'][0].keys()
        print(list(obje))

        if (
            len(response.get("operacoes")) != 0 or
            len(response.get("desembolsos")) != 0 or
            len(response.get("carteira")) != 0
        ):
            BNDES.response = response

    @classmethod
    def store_bndes_response(cls, response, client):
        """Method for storing BNDES response("operacoes") in OPERACOES model

        Args:
            response(dict) : BNDES response, 
        """

        serializer_data = {}
        serializer_data["client"] = client.cnpj_id
        serializer_data["logs"] = response

        serializer = serializers.BNDESOperacoesSerializers(
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
        old_data = BNDESOperacoes.objects.get(client=client)

        serializer_data = {}
        serializer_data["client"] = client
        serializer_data["logs"] = old_data.logs

        serializer = serializers.ArchiveBNDESOperacoesSerializers(
            data=serializer_data
        )
        print("objeto do lixo criado")
        serializer.is_valid()
        serializer.save()
        params.delete()
        return None

    @classmethod
    def store_bndes_response_oper(cls,):
        pass
