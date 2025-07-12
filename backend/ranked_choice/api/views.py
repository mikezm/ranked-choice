from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ranked_choice.api.serializers import (
    BallotDetailSerializer,
    BallotResultSerializer,
    CreateBallotSerializer,
    CreateVoterSerializer,
)
from ranked_choice.core.domain.workflows.create_ballot_workflow import (
    create_ballot_workflow,
)
from ranked_choice.core.domain.workflows.create_vote_workflow import (
    create_vote_workflow,
)
from ranked_choice.core.domain.workflows.get_ballot_workflow import get_ballot_workflow
from ranked_choice.core.domain.workflows.get_votes_workflow import get_votes_workflow
from ranked_choice.core.domain.workflows.list_ballots_workflow import (
    list_ballots_workflow,
)


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
    Create a new ballot with the given title, choices, and optional description.
    """
    serializer = CreateBallotSerializer(data=request.data)

    if serializer.is_valid():
        # Get validated data
        title = serializer.validated_data['title']
        description = serializer.validated_data.get('description', None)
        choices = serializer.validated_data.get('choices', None)

        try:
            # Call workflow and get the slug
            slug = create_ballot_workflow(
                title=title,
                choices=choices,
                description=description
            )

            # Return response with only the slug
            return Response({
                "slug": slug
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_ballot(request, slug):
    """
        Retrieve a ballot using its slug from the URL path.

        Args:
            request: The HTTP request object
            slug: The unique identifier for the ballot

        Returns:
            Response with serialized ballot data or the appropriate error message
        """
    try:
        ballot_item = get_ballot_workflow(slug=slug)

        if ballot_item is None:
            return Response(
                {"error": "Ballot not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BallotDetailSerializer(ballot_item)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception:
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def create_vote(request):
    """
    Create a new ballot with the given title, choices, and optional description.
    """
    serializer = CreateVoterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    name = serializer.validated_data['name']
    ballot_id = serializer.validated_data['ballot_id']
    votes = serializer.validated_data['votes']

    try:
        create_vote_workflow(name=name, ballot_id=ballot_id, votes=votes)
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def list_ballots(request):
    """
    Retrieve all ballots.

    Args:
        request: The HTTP request object

    Returns:
        Response with serialized list of ballots or the appropriate error message
    """
    try:
        ballot_items = list_ballots_workflow()
        serializer = BallotDetailSerializer(ballot_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception:
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_votes(request, slug):
    """
        Retrieve votes for a ballot

        Args:
            request: The HTTP request object
            slug: The unique identifier for the ballot

        Returns:
            Response with serialized ballot data or the appropriate error message
        """
    try:
        results = get_votes_workflow(slug=slug)

        if results is None:
            return Response(
                {"error": "Ballot not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BallotResultSerializer(results)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": "Internal server error", "error_details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
