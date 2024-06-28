from django.http import JsonResponse
from .models import ToDoList
from .serializers import ToDoListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def todolist_list(request, format=None):
    if request.method == 'GET':
        tasks = ToDoList.objects.all()
        serializer = ToDoListSerializer(tasks, many=True)
        return Response({"tasks": serializer.data})

    if request.method == 'POST':
        serializer = ToDoListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def todolist_detail(request, id, format=None):

    try:
        task = ToDoList.objects.get(pk=id)
    except ToDoList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ToDoListSerializer(task)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ToDoListSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
