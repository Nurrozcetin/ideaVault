from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Idea
from .serializer import IdeaSerializer

@api_view(['GET', 'POST'])
def ideas(request, format=None):
    if request.method == "GET":
        ideas = Idea.objects.all()
        serializer = IdeaSerializer(ideas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = IdeaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def ideas_id(request, id):
    try:
        idea = Idea.objects.get(pk=id)
    except Idea.DoesNotExist:
        return Response({"error": "No matching record found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = IdeaSerializer(idea)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = IdeaSerializer(idea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        idea.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
