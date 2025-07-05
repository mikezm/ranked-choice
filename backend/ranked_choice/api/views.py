from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from ranked_choice.api.serializers import CreateBallotSerializer
from ranked_choice.core.repositories.ballot_repository import BallotRepository
from ranked_choice.core.workflows.ballot_workflows import create_new_ballot


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
    Create a new ballot with the given title and optional description.
    """
    serializer = CreateBallotSerializer(data=request.data)

    if serializer.is_valid():
        # Get validated data
        title = serializer.validated_data['title']
        description = serializer.validated_data.get('description', None)

        try:
            # Create repository
            ballot_repository = BallotRepository()

            # Call workflow
            ballot = create_new_ballot(
                ballot_repository=ballot_repository,
                title=title,
                description=description
            )

            # Return response
            return Response({
                "id": ballot.id,
                "slug": ballot.slug,
                "title": ballot.title,
                "created_at": ballot.created_at,
                "updated_at": ballot.updated_at
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
