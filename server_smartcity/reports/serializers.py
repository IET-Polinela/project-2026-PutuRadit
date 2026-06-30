from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    reporter_name = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'title',
            'description',
            'location',
            'category',
            'status',
            'created_at',
            'updated_at',
            'reporter',
            'reporter_name',
            'is_owner',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'reporter',
            'reporter_name',
            'is_owner',
        ]

    def get_reporter(self, obj) -> str:
        return 'Warga Anonim'

    def get_reporter_name(self, obj) -> str:
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            if obj.reporter_id == request.user.id:
                return obj.reporter.username

        return 'Warga Anonim'

    def get_is_owner(self, obj) -> bool:
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return obj.reporter_id == request.user.id
