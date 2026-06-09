from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):

    # tampilkan anonim saat GET
    reporter = serializers.SerializerMethodField(
        read_only=True
    )

    # Lab 12
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report

        fields = [
            'id',
            'reporter',
            'title',
            'description',
            'location',
            'category',
            'status',
            'created_at',
            'updated_at',
            'is_owner',
        ]

        read_only_fields = [
            'reporter',
            'created_at',
            'updated_at',
            'is_owner',
        ]


    def get_reporter(self, obj):

        return "Warga Anonim"


    def get_is_owner(self, obj):

        request = self.context.get('request')

        if (
            request and
            request.user and
            request.user.is_authenticated
        ):
            return obj.reporter == request.user

        return False
