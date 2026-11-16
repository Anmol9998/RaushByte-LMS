from mentors.models import MentorProfile


class MentorContextMiddleware:
    """
    Attach the authenticated mentor's profile to the request as ``request.mentor_profile``.

    This keeps views/permissions from re-querying the profile and centralises the
    "derive the current mentor from request.user" rule (never trust a frontend
    mentor_id). Non-mentor users get ``request.mentor_profile = None``.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.mentor_profile = None
        if getattr(request, "user", None) and request.user.is_authenticated:
            try:
                if getattr(request.user, "role", None) == "mentor":
                    request.mentor_profile = (
                        MentorProfile.objects.filter(user=request.user).first()
                    )
            except Exception:
                # Never let a context lookup break the request cycle.
                request.mentor_profile = None
        return self.get_response(request)