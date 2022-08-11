from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from BNDESIntegration.serializers import BNDESTransactionSerializers
from rest_framework import (
    generics,
    response,
    status
)
from BNDESIntegration.bndes_requests import BNDES
# Create your views here.


class BNDESDatasetGetView(generics.GenericAPIView):
    """VIEW to get BNDES operation data

    Args:
        request.data (JSON): HTTP request data

    Returns:
        dict : Query results
    """
    serializer_class = BNDESTransactionSerializers

    def get(self, request, cnpj, name):
        """GET BNDES data.

        Args:
            request.data (JSON): HTTP request data
            cnpj (string): CNPJ client
            name (string): Type of request (operacoes, desembolsos or all)
        Returns 
            returnDict : BNDES serialized results
        """

        bndes_response = BNDES.get_bndes_data(request, cnpj)

        if bndes_response:
            if name.lower() == 'all':
                return JsonResponse(bndes_response, safe=False)

            elif bndes_response[name]:
                return JsonResponse(bndes_response[name], safe=False)

            else:
                return response.Response(f'NULL: {request.data}', status.HTTP_404_NOT_FOUND)

        else:
            return response.Response(f'Error while trying to receive data from: {request.data}',
                                     status.HTTP_404_NOT_FOUND
                                     )


class BNDESIntegrationDetailView(generics.GenericAPIView):
    """VIEW to get BNDES operation data and show in each operation

    Args:
        request.data (JSON): HTTP request data

    Returns:
        dict : Query results
    """
    serializer_class = BNDESTransactionSerializers

    def get(self, request, cnpj, name, id):
        """ GET BNDES DATA and OPERATION NUMBER

        Args:
            request.data (JSON): HTTP request data
            cnpj (string): CNPJ client
            name (string): Type of request (operacoes, desembolsos or all)
        Returns 
            returnDict : BNDES serialized results

        """

        bndes_response = BNDES.get_bndes_data(request, cnpj)
        try:
            if bndes_response:
                if name.lower() == 'all':
                    return JsonResponse(bndes_response, safe=False)

                elif bndes_response[name][int(id)]:
                    return JsonResponse(bndes_response[name][int(id)], safe=False)
            else:
                return response.Response(f'Error while trying to receive data from: {request.data}',
                                         status.HTTP_404_NOT_FOUND
                                         )
        except IndexError:
            return response.Response(f'Error while trying to receive data from: {request.data}',
                                     status.HTTP_404_NOT_FOUND
                                     )
