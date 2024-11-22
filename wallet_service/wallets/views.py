from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet
from .serializers import WalletSerializer, OperationSerializer
from django.shortcuts import get_object_or_404
from .tasks import process_wallet_operation
from django.http import Http404


class WalletDetailView(APIView):
    def get(self, request, wallet_id):
        try:
            wallet = get_object_or_404(Wallet, wallet_id=wallet_id)
        except Http404:
            return Response(
                {'error': 'Кошелек с таким UUID не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WalletOperationView(APIView):
    def post(self, request, wallet_id):
        data = request.data.copy()
        data['wallet_id'] = wallet_id
        serializer = OperationSerializer(data=data)

        if serializer.is_valid():
            operation_type = serializer.validated_data['operation_type']
            amount = serializer.validated_data['amount']
            task = process_wallet_operation.apply_async(
                args=(wallet_id, operation_type, amount)
            )
            return Response(
                {
                    'message': 'Операция в процессе. '
                               'ID задачи: {}'.format(task.id)
                },
                status=status.HTTP_202_ACCEPTED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
