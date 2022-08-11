from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from BNDESIntegration.serializers import BNDESOperacoesSerializers
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
    serializer_class = BNDESOperacoesSerializers

    def get(self, request, cnpj, nome):
        """GET BNDES data.

        Args:
            request.data (JSON): HTTP request data
        Returns 
            returnDict : BNDES serialized results
        """

        bndes_response = BNDES.get_bndes_data(request, cnpj)
        if nome.lower() == 'all':
            return JsonResponse(bndes_response, safe=False)
        elif bndes_response[nome]:
            return JsonResponse(bndes_response[nome], safe=False)
        else:
            return response.Response(f'Error while trying to receive data from: {request.data}',
                                     status.HTTP_404_NOT_FOUND
                                     )
