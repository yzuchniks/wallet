import logging

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet
from .serializers import OperationSerializer, WalletSerializer
from .tasks import process_wallet_operation
from .utils import check_request_limit

logger = logging.getLogger(__name__)


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
        try:
            check_request_limit(wallet_id)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)
        logger.debug(f'Начало обработки операции для кошелька {wallet_id}')
        data = request.data.copy()
        data['wallet_id'] = wallet_id
        serializer = OperationSerializer(data=data)

        if serializer.is_valid():
            logger.debug(f'Сериализатор валиден: {serializer.validated_data}')
            operation_type = serializer.validated_data['operation_type']
            amount = serializer.validated_data['amount']
            task = process_wallet_operation.apply_async(
                args=(wallet_id, operation_type, amount)
            )
            logger.debug(f'Задача запущена, ID: {task.id}')
            return Response(
                {
                    'message': 'Операция в процессе.',
                    'task_id': task.id
                },
                status=status.HTTP_202_ACCEPTED
            )
        logger.warning(f'Сериализатор невалиден: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
