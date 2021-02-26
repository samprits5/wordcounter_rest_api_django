from django.shortcuts import render
from django.http import JsonResponse


from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Counter
from .serializers import CounterSerializer


def index(request):
    return JsonResponse({'info':'Count Word API v1', 'developer':'Samprit Sarkar'})


@api_view(['GET', 'POST'])
def count_word(request):
    if request.method == 'GET':

        data = Counter.objects.all()

        serializer = CounterSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        if not 'text' in request.data.keys():
            return Response({'detail':'No text parameter found.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        
        text_data = data['text']

        no_of_words = len(text_data.split())

        data['total_words'] = no_of_words

        serializer = CounterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def count_word_each(request, pk):

    try:
        record = Counter.objects.get(pk=pk)

    except Counter.DoesNotExist:
        return Response({'detail':'No such record exists.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CounterSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':

        if not 'text' in request.data.keys():
            return Response({'detail':'No text parameter found.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        
        text_data = data['text']

        no_of_words = len(text_data.split())

        data['total_words'] = no_of_words

        serializer = CounterSerializer(record, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        record.delete()
        return Response({'detail':'Record Deleted'}, status=status.HTTP_200_OK)


 