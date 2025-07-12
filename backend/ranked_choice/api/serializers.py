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


class BallotChoiceSerializer(serializers.Serializer):
    """
    Serializer for ballot choices in the response.
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)


class BallotDetailSerializer(serializers.Serializer):
    """
    Serializer for ballot details in the response.
    """
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    choices = BallotChoiceSerializer(many=True)


class VoteSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    choice_id = serializers.IntegerField()


class CreateVoterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    ballot_id = serializers.IntegerField()
    votes = VoteSerializer(many=True, required=True)

    def validate_votes(self, value):
        """
        Check that the votes list is not empty.
        """
        if not value:
            raise serializers.ValidationError("At least one vote must be provided.")
        return value
