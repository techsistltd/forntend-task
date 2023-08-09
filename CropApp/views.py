from drf_spectacular.utils import extend_schema, OpenApiExample
from nested_multipart_parser import NestedParser
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.pagination import CustomPagination
from utils.query_params_manager import set_query_params
from .models import *
from .serializers import *
from django.db import transaction
from utils.validator import bool_validator
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser


@extend_schema(tags=["Crops Category"])
class CropsCategoryViewSet(viewsets.ModelViewSet):
    queryset = CropsCategoryModel.objects.all()
    serializer_class = CropsCategorySerializer
    lookup_field = "id"


@extend_schema(tags=["Crops"])
class CropsViewSet(viewsets.ModelViewSet):
    queryset = CropsModel.objects.all()
    serializer_class = CropsSerializer
    lookup_field = "id"
    pagination_class = CustomPagination
    # parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == "list":
            return CropsListSerializer
        elif self.action == "retrieve":
            return CropsRetrieveSerializer
        else:
            return CropsSerializer

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create crops",
                value={
                    "title": "string",
                    "image": "string",
                    "description": "string",
                    "category": 0,
                    "disease": [{"title": "string", "image": "file"}],
                },
                request_only=True,
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        diseases = request.data.pop("disease", None)
        diseases_list = []
        if diseases:
            for disease in diseases:
                disease_title = disease.get("title", None)
                disease_image = disease.get("image", None)
                data = {
                    "title": disease_title,
                    "image": disease_image
                }
                disease_obj = DiseasesModel.objects.create(data)
                if disease_obj.id not in diseases_list:
                    diseases_list.append(disease_obj.id)

        # validate_data["image"] = validate_data["image"]
        request.data["disease"] = diseases_list if diseases_list else None
        crops_serializer = CropsSerializer(data=request.data, files=request.FILES)
        if crops_serializer.is_valid(raise_exception=True):
            crops_obj = crops_serializer.save()
            crops_data = CropsListSerializer(crops_obj, many=False).data
            crops_data["detail"] = "ফসল সফলভাবে তৈরি করা হয়েছে"
            return Response(data=crops_data, status=status.HTTP_200_OK)
        return Response(data={"detail": "ভুল তথ্য দেয়া হয়েছে, দয়া করে সঠিক তথ্য প্রদান করুন । "},
                        status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=set_query_params('list', [
            {"name": 'category', "description": 'category id'},
            {'name': 'is_archived', 'type': 'bool', "description": 'Archived or not', 'required': False},
            {'name': 'page', 'type': 'int', 'required': False},
            {'name': 'page_size', 'type': 'int', 'required': False}
        ])
    )
    def list(self, request, *args, **kwargs):
        is_archived = request.query_params.get("is_archived") == "true"
        category = request.query_params.get("category")
        if category:
            self.queryset = self.queryset.filter(category=category)
        if 'is_archived' in request.query_params.keys():
            self.queryset = self.queryset.filter(is_archived=is_archived)
        paginator = self.pagination_class()
        serializer_class = self.get_serializer_class()
        page = paginator.paginate_queryset(self.queryset, request)
        serializer = serializer_class(
            page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('id', None)
        if not pk:
            raise ValidationError("Invalid Crops")
        crops_obj = None
        try:
            crops_obj = CropsModel.objects.get(pk=pk)
        except CropsModel.DoesNotExist:
            raise ValidationError()

        diseases = request.data.pop('disease', None)
        diseases_list = []
        if diseases:
            for disease in diseases:
                disease_id = disease.pop('id', None)
                disease_title = disease.get("title", None)
                disease_image = disease.get("image", None)
                if disease_id:
                    try:
                        disease_obj = DiseasesModel.objects.get(pk=disease_id)
                        if type(disease["image"]) == str:
                            disease_image = None
                        if disease_image:
                            DiseasesModel.objects.filter(pk=disease_id).update(
                                title=disease_title, image=disease_image)
                        else:
                            DiseasesModel.objects.filter(pk=disease_id).update(title=disease_title)
                        disease_obj = DiseasesModel.objects.get(pk=disease_id)
                    except Exception as e:
                        raise ValidationError(e)
                else:
                    data = {
                        "title": disease_title,
                        "image": disease_image
                    }
                    disease_obj = DiseasesModel.objects.create(**data)
                if disease_obj.id not in diseases_list:
                    diseases_list.append(disease_obj.id)

        request.data["disease"] = diseases_list if diseases_list else None
        if type(request.data["image"]) == str:
            request.data.pop('image')
        crops_serializer = self.serializer_class(
            data=request.data, instance=crops_obj)
        if crops_serializer.is_valid(raise_exception=True):
            crops_obj = crops_serializer.save()
            crops_data = CropsListSerializer(crops_obj, many=False).data
            crops_data["detail"] = "ফসল সফলভাবে আপডেট  করা হয়েছে"
            return Response(data=crops_data, status=status.HTTP_200_OK)
        return Response(data={"detail": "ভুল তথ্য দেয়া হয়েছে, দয়া করে সঠিক তথ্য প্রদান করুন । "},
                        status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        obj = self.queryset.filter(pk=pk).first()
        if obj:
            serializer = CropsRetrieveSerializer(
                obj, many=False, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            raise ValidationError("Invalid Crops")


@extend_schema(tags=["Crops Disease"])
class DiseaseViewSet(viewsets.ModelViewSet):
    queryset = DiseasesModel.objects.all()
    serializer_class = DiseaseSerializer
    lookup_field = "id"


@extend_schema(tags=["Archive"])
class ArchiveManagerAPIView(CreateAPIView):
    serializer_class = Archiveserializer

    @extend_schema(
        examples=[
            OpenApiExample(
                "Archive",
                value={
                    "usercropsdiseases": [1, 2]
                },
                request_only=True,
            )
        ],
        parameters=set_query_params('list', [
            {"name": 'is_archived', "description": 'Is archive means True and not archived means false',
             'type': 'bool'},
        ])
    )
    def post(self, request, *args, **kwargs):
        query_param = request.query_params.get("is_archived")
        is_archived = bool_validator(query_param)[0]
        if query_param:
            crops_list = request.data.get("usercropsdiseases", [])

            CropsModel.objects.filter(id__in=crops_list).update(
                is_archived=is_archived
            )
            if is_archived:
                return Response("Items archived success.", status=status.HTTP_200_OK)

            elif not is_archived:
                return Response("Items unarchived success.", status=status.HTTP_200_OK)
            else:
                return Response(
                    "Invalid archive type", status=status.HTTP_400_BAD_REQUEST
                )
        else:
            raise PermissionDenied('Method not allowed.')
