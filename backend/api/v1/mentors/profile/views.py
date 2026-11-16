from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from mentors.models import MentorProfile
from .serializers import MentorProfileSerializer, PublicMentorProfileSerializer
from .permissions import IsMentor, IsMentorOwner


def _mentor_forbidden_response():
    return Response(
        {"detail": "Forbidden: only mentors can access this endpoint."},
        status=status.HTTP_403_FORBIDDEN,
    )


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve logged-in mentor profile",
        operation_id="mentors_profile_retrieve_own",
        responses={
            200: MentorProfileSerializer,
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="User is not a mentor"),
            404: OpenApiResponse(description="Profile does not exist"),
        },
        tags=["Mentor Profile"],
    ),
    post=extend_schema(
        summary="Create mentor profile",
        request=MentorProfileSerializer,
        responses={
            201: MentorProfileSerializer,
            400: OpenApiResponse(description="Invalid profile data"),
            403: OpenApiResponse(description="User is not a mentor"),
            409: OpenApiResponse(description="Duplicate profile creation"),
        },
        tags=["Mentor Profile"],
    ),
)
class MentorProfileView(APIView):
    permission_classes = [IsMentor]
    serializer_class = MentorProfileSerializer

    def get_object(self):
        try:
            return MentorProfile.objects.get(user=self.request.user)
        except MentorProfile.DoesNotExist:
            return None

    def get(self, request):
        profile = self.get_object()
        if not profile:
            return Response(
                {"detail": "Profile does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(MentorProfileSerializer(profile).data, status=status.HTTP_200_OK)

    def post(self, request):
        if MentorProfile.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "Profile already exists."},
                status=status.HTTP_409_CONFLICT,
            )
        serializer = MentorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = self.get_object()
        if not profile:
            return Response(
                {"detail": "Profile does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if profile.is_deleted:
            return Response(
                {"detail": "Mentor account is deactivated. Block profile modifications."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = MentorProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        profile = self.get_object()
        if not profile:
            return Response(
                {"detail": "Profile does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if profile.is_deleted:
            return Response(
                {"detail": "Mentor account is deactivated. Block profile modifications."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = MentorProfileSerializer(profile, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        profile = self.get_object()
        if not profile:
            return Response(
                {"detail": "Profile does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Soft-deactivate profile only; do not delete the CustomUser.
        profile.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="View a public mentor profile",
    parameters=[
        OpenApiParameter(
            name="mentor_id",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description="Mentor profile ID",
        ),
    ],
    responses={
        200: PublicMentorProfileSerializer,
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(description="Profile does not exist"),
    },
    tags=["Mentor Profile"],
)
class PublicMentorProfileView(generics.RetrieveAPIView):
    permission_classes = [IsMentor]
    queryset = MentorProfile.objects.filter(is_deleted=False)
    serializer_class = PublicMentorProfileSerializer
    lookup_url_kwarg = "mentor_id"

    def get_object(self):
        mentor_id = self.kwargs.get(self.lookup_url_kwarg)
        try:
            return MentorProfile.objects.get(id=mentor_id, is_deleted=False)
        except MentorProfile.DoesNotExist:
            from rest_framework.exceptions import NotFound

            raise NotFound("Profile does not exist.")