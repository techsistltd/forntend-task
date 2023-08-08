from rest_framework import serializers
from .models import *


from .models import *


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseasesModel
        fields = "__all__"
        extra_kwargs = {"slug": {"read_only": True}}


class DiseaseRetrieveSerializer(serializers.ModelSerializer):
    crop = serializers.SerializerMethodField()
    medicine = serializers.SerializerMethodField()

    class Meta:
        model = DiseasesModel
        fields = "__all__"
        extra_kwargs = {"slug": {"read_only": True}}


class CropsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CropsCategoryModel
        fields = "__all__"
        extra_kwargs = {"slug": {"read_only": True}}


class CropsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropsModel
        fields = "__all__"
        extra_kwargs = {"slug": {"read_only": True}}


class CropsListSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer(read_only=True, many=True)

    class Meta:
        model = CropsModel
        fields = "__all__"
        extra_kwargs = {"slug": {"read_only": True}}


class CropsRetrieveSerializer(serializers.ModelSerializer):
    category = CropsCategorySerializer(read_only=True, many=False)
    disease = DiseaseSerializer(read_only=True, many=True)

    class Meta:
        model = CropsModel
        fields = "__all__"
        extra_kwargs = {"slug": {"read_only": True}}


class Archiveserializer(serializers.Serializer):
    usercropsdiseases = serializers.ListField()
