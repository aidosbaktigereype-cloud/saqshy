"""Сводка на главной странице CRM: заявки, источники, воронка, просроченные шаги."""

from datetime import timedelta

from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from crm.models import OPEN_STATUSES, Lead, LeadSource, LeadStatus


def percent(part: int, total: int) -> int:
    return round(part * 100 / total) if total else 0


def dashboard_callback(request, context):
    now = timezone.now()
    today = timezone.localtime(now).replace(hour=0, minute=0, second=0, microsecond=0)
    month_ago = now - timedelta(days=30)
    leads = Lead.objects.all()
    month = leads.filter(created_at__gte=month_ago)
    month_total = month.count()

    sources = dict(month.values_list("source").annotate(n=Count("id")).values_list("source", "n"))
    by_source = sorted(
        (
            {"label": label, "count": sources.get(code, 0), "pct": percent(sources.get(code, 0), month_total)}
            for code, label in LeadSource.choices
            if sources.get(code)
        ),
        key=lambda row: -row["count"],
    )

    statuses = dict(leads.values_list("status").annotate(n=Count("id")).values_list("status", "n"))
    open_total = sum(statuses.get(s, 0) for s in OPEN_STATUSES)
    funnel = [
        {"code": code, "label": label, "count": statuses.get(code, 0), "pct": percent(statuses.get(code, 0), open_total)}
        for code, label in LeadStatus.choices
        if code in OPEN_STATUSES
    ]

    days = 14
    start = today - timedelta(days=days - 1)
    per_day = dict(
        leads.filter(created_at__gte=start)
        .annotate(day=TruncDate("created_at", tzinfo=timezone.get_current_timezone()))
        .values_list("day")
        .annotate(n=Count("id"))
        .values_list("day", "n")
    )
    peak = max(per_day.values(), default=0)
    daily = []
    for i in range(days):
        day = (start + timedelta(days=i)).date()
        count = per_day.get(day, 0)
        daily.append({"label": day.strftime("%d.%m"), "count": count, "pct": percent(count, peak)})

    done_month = month.filter(status=LeadStatus.DONE)
    context["dash"] = {
        "today": leads.filter(created_at__gte=today).count(),
        "week": leads.filter(created_at__gte=now - timedelta(days=7)).count(),
        "month": month_total,
        "open": open_total,
        "unassigned": leads.filter(status=LeadStatus.NEW, assignee__isnull=True).count(),
        "overdue": leads.filter(status__in=OPEN_STATUSES, next_action_at__lt=now).count(),
        "conversion": percent(done_month.count(), month_total),
        "revenue": done_month.aggregate(s=Sum("amount"))["s"] or 0,
        "by_source": by_source,
        "funnel": funnel,
        "daily": daily,
        "recent": leads.select_related("service", "assignee")[:8],
        "my_overdue": leads.filter(assignee=request.user, status__in=OPEN_STATUSES, next_action_at__lt=now)
        .select_related("service")
        .order_by("next_action_at")[:5],
    }
    return context
