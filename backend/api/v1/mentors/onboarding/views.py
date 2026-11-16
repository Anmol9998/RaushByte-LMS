from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from mentors.models import (
    MentorOnboardingApplication,
    MentorOnboardingDocument,
)
from .serializers import (
    MentorOnboardingApplicationSerializer,
    MentorOnboardingDocumentSerializer,
    OnboardingDocumentUploadSerializer,
    AdminOnboardingActionSerializer,
)
from .permissions import IsMentor, IsAdminRole


class MentorOnboardingApplicationView(APIView):
    permission_classes = [IsMentor]

    def get_application(self, request):
        return (
            MentorOnboardingApplication.objects.filter(user=request.user)
            .order_by("-created_at")
            .first()
        )

    @extend_schema(
        summary="Submit mentor onboarding application",
        request=MentorOnboardingApplicationSerializer,
        responses={
            201: MentorOnboardingApplicationSerializer,
            400: OpenApiResponse(description="Invalid onboarding data"),
            403: OpenApiResponse(description="User is not a mentor"),
            409: OpenApiResponse(description="Application already submitted"),
        },
        tags=["Mentor Onboarding"],
    )
    def post(self, request):
        existing = self.get_application(request)
        if existing and existing.status in (
            "SUBMITTED",
            "UNDER_REVIEW",
            "APPROVED",
        ):
            return Response(
                {"detail": "An onboarding application already exists."},
                status=status.HTTP_409_CONFLICT,
            )
        serializer = MentorOnboardingApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, status="DRAFT")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Update pending application",
        request=MentorOnboardingApplicationSerializer,
        responses={
            200: MentorOnboardingApplicationSerializer,
            400: OpenApiResponse(description="Invalid data"),
            403: OpenApiResponse(description="Cannot edit after approval"),
        },
        tags=["Mentor Onboarding"],
    )
    def patch(self, request):
        application = self.get_application(request)
        if not application:
            return Response(
                {"detail": "No onboarding application found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if application.status not in ("DRAFT", "NEEDS_CORRECTION"):
            return Response(
                {
                    "detail": "Cannot edit an application in %s status."
                    % application.status
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = MentorOnboardingApplicationSerializer(
            application, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
class MentorOnboardingStatusView(APIView):
    permission_classes = [IsMentor]

    @extend_schema(
        summary="Check onboarding status",
        responses={
            200: MentorOnboardingApplicationSerializer,
            404: OpenApiResponse(description="No application found"),
        },
        tags=["Mentor Onboarding"],
    )
    def get(self, request):
        application = (
            MentorOnboardingApplication.objects.filter(user=request.user)
            .order_by("-created_at")
            .first()
        )
        if not application:
            return Response(
                {"detail": "No onboarding application found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            MentorOnboardingApplicationSerializer(application).data,
            status=status.HTTP_200_OK,
        )


class MentorOnboardingDocumentListCreateView(APIView):
    permission_classes = [IsMentor]

    def get_application(self, request):
        return (
            MentorOnboardingApplication.objects.filter(user=request.user)
            .order_by("-created_at")
            .first()
        )

    @extend_schema(
        summary="View submitted documents",
        responses={
            200: MentorOnboardingDocumentSerializer(many=True),
            403: OpenApiResponse(description="User is not a mentor"),
            404: OpenApiResponse(description="No application found"),
        },
        tags=["Mentor Onboarding"],
    )
    def get(self, request):
        application = self.get_application(request)
        if not application:
            return Response(
                {"detail": "No onboarding application found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        documents = MentorOnboardingDocument.objects.filter(
            application=application, is_deleted=False
        )
        return Response(
            MentorOnboardingDocumentSerializer(documents, many=True).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Upload verification documents",
        request=OnboardingDocumentUploadSerializer,
        responses={
            201: MentorOnboardingDocumentSerializer,
            400: OpenApiResponse(description="Invalid document data"),
            403: OpenApiResponse(description="User is not a mentor"),
            404: OpenApiResponse(description="No application found"),
        },
        tags=["Mentor Onboarding"],
    )
    def post(self, request):
        application = self.get_application(request)
        if not application:
            return Response(
                {"detail": "No onboarding application found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if application.status not in ("DRAFT", "NEEDS_CORRECTION", "SUBMITTED"):
            return Response(
                {
                    "detail": "Cannot upload documents for an application in %s status."
                    % application.status
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = OnboardingDocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            document = MentorOnboardingDocument.objects.create(
                application=application,
                document_type=serializer.validated_data["document_type"],
                file_url=serializer.validated_data["file_url"],
                file_name=serializer.validated_data.get("file_name", ""),
                file_size=serializer.validated_data.get("file_size"),
            )
            return Response(
                MentorOnboardingDocumentSerializer(document).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MentorOnboardingDocumentDeleteView(APIView):
    permission_classes = [IsMentor]

    @extend_schema(
        summary="Remove document before submission",
        parameters=[
            OpenApiParameter(
                name="doc_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Document ID",
            ),
        ],
        responses={
            204: None,
            403: OpenApiResponse(description="User is not a mentor"),
            404: OpenApiResponse(description="Document not found"),
        },
        tags=["Mentor Onboarding"],
    )
    def delete(self, request, doc_id):
        try:
            document = MentorOnboardingDocument.objects.get(id=doc_id)
        except MentorOnboardingDocument.DoesNotExist:
            return Response(
                {"detail": "Document not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        application = document.application
        if str(application.user.id) != str(request.user.id):
            return Response(
                {"detail": "You cannot access another applicant's documents."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if application.status not in ("DRAFT", "NEEDS_CORRECTION"):
            return Response(
                {
                    "detail": "Cannot remove documents for an application in %s status."
                    % application.status
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        document.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)