from rest_framework import serializers


class CreateBallotSerializer(serializers.Serializer):
    """
    Serializer for creating a new ballot.
    """
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)