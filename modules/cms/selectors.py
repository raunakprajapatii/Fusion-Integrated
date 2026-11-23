"""Read paths with ownership scoping applied before data is returned."""

from django.db.models import Q

from modules.cms.models import CmsRoleAssignment, Complaint


def complaints_for(actor, *, role=None):
    qs = Complaint.objects.all().prefetch_related(
        "attachments", "history", "progress_updates", "reopening_requests"
    )
    if role == "supervisor":
        return qs
    if role == "handler":
        return qs.filter(
            Q(assigned_handler_user_id=actor.user_id) | Q(assigned_handler_user_id__isnull=True)
        )
    return qs.filter(complainant_user_id=actor.user_id)


def has_active_role(user_id: int, role: str, *, at=None) -> bool:
    from django.utils import timezone

    at = at or timezone.now()
    return CmsRoleAssignment.objects.filter(
        user_id=user_id, role=role, is_active=True, starts_at__lte=at, ends_at__gt=at
    ).exists()
