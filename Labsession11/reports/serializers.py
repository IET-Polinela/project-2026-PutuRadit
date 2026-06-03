from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):

    # tampilkan anonim saat GET
    reporter = serializers.SerializerMethodField(
        read_only=True
    )

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
        ]

        read_only_fields = [
            'reporter',
            'created_at',
            'updated_at',
        ]


    def get_reporter(self, obj):

        return "Warga Anonim"
