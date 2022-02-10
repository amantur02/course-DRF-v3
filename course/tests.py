from django.test import TestCase

from django.http import JsonResponse
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from course.models import Course
from course.serializers import CourseSerializer
from course.services import CourseService
from course.validators import CourseValidator


class CourseCreateListAPIView(generics.CreateAPIView):
    # queryset = Course.objects.all()
    # serializer_class = CourseSerializer
    validator_class = CourseValidator
    service_class = CourseService

    def post(self, request, *args, **kwargs):
        data = request.data

        if self.validator_class.validator_br_con(contacts=data['contacts'], branches=data['branches']):
            con_br_id = self.service_class.create_con_br(contacts=data['contacts'], branches=data['branches'])

            data['contacts'] = con_br_id['con']
            data['branches'] = con_br_id['br']

            serializer = CourseSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return Response('Error: You wrote the data incorrectly or you do not have enough amount')