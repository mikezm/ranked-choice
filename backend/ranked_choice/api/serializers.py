from rest_framework import serializers


class ChoiceSerializer(serializers.Serializer):
    """
    Serializer for ballot choices.
    """
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)


class CreateBallotSerializer(serializers.Serializer):
    """
    Serializer for creating a new ballot.
    """
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    choices = ChoiceSerializer(many=True, required=True)

    def validate_choices(self, value):
        """
        Check that the choices list is not empty.
        """
        if not value:
            raise serializers.ValidationError("At least one choice must be provided.")
        return value
