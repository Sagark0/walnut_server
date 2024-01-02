from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TransactionSerializer
from . import scripts
from .models import Transaction

def index(request):
    return HttpResponse("Transaction server is hosted")

@api_view(['GET'])
def getMails(request):
    transaction = Transaction.objects.all().order_by('-date')
    serializer = TransactionSerializer(transaction, many=True)
    return Response(serializer.data)

def fetchMails(request):
    existing_transaction_ids = Transaction.objects.values('transaction_id')
    existing_transaction_ids = set([t["transaction_id"] for t in existing_transaction_ids])
    mails = scripts.gmail(existing_transaction_ids)
    data_list = [ Transaction(**data) for data in mails]
    Transaction.objects.bulk_create(data_list)
    return HttpResponse("Fetching Mails")

def updateCategory(request):
    transaction_id = request.GET.get('transaction_id', None)
    category = request.GET.get('category', None)
    transaction = Transaction.objects.get(transaction_id = transaction_id)
    transaction.category = category
    transaction.save()
    return JsonResponse({'status': 'success'})