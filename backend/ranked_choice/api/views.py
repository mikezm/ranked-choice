from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from ranked_choice.api.serializers import CreateBallotSerializer
from ranked_choice.core.repositories.ballot_repository import BallotRepository
from ranked_choice.core.domain.workflows.create_ballot_workflow import create_ballot_workflow


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    A simple health check endpoint to verify the API is working.
    """
    return Response({"status": "ok"})


@api_view(['POST'])
@permission_classes([AllowAny])
def create_ballot(request):
    """
    Create a new ballot with the given title, optional description, and optional choices.
    """
    serializer = CreateBallotSerializer(data=request.data)

    if serializer.is_valid():
        # Get validated data
        title = serializer.validated_data['title']
        description = serializer.validated_data.get('description', None)
        choices = serializer.validated_data.get('choices', None)

        try:
            # Create repository
            ballot_repository = BallotRepository()

            # Call workflow and get the slug
            slug = create_ballot_workflow(
                ballot_repository=ballot_repository,
                title=title,
                description=description,
                choices=choices
            )

            # Return response with only the slug
            return Response({
                "slug": slug
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
