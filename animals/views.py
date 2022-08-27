from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from .models import Animal
from .serializers import AnimalSerializer


class AnimalView(APIView):
    def post(self, request: Request) -> Response:
        serializer = AnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class AnimalDetailView(APIView):

    def patch(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except ValidationError as err:
            return Response(str(err), status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(serializer.data, status.HTTP_200_OK)

    def get(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        animal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

