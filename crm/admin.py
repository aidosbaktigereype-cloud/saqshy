from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from crm.models import Lead, LeadEvent, LeadStatus, StaffProfile

STATUS_COLORS = {
    LeadStatus.NEW: "info",
    LeadStatus.IN_WORK: "warning",
    LeadStatus.MEASURE: "warning",
    LeadStatus.PROPOSAL: "primary",
    LeadStatus.INSTALL: "primary",
    LeadStatus.DONE: "success",
    LeadStatus.LOST: "danger",
}


class LeadForm(forms.ModelForm):
    new_comment = forms.CharField(
        label="Добавить комментарий",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        help_text="Попадёт в историю заявки",
    )

    class Meta:
        model = Lead
        fields = "__all__"


class LeadEventInline(TabularInline):
    model = LeadEvent
    extra = 0
    can_delete = False
    fields = ("created_at", "kind", "text", "author")
    readonly_fields = fields
    verbose_name_plural = "История"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    form = LeadForm
    inlines = [LeadEventInline]
    list_display = ("number", "created_at", "show_status", "name", "phone_link", "service", "source", "assignee", "next_action_at")
    list_display_links = ("number", "name")
    list_filter = ("status", "source", "service", "assignee", "locale", "created_at")
    list_filter_submit = True
    search_fields = ("name", "phone", "message", "utm_campaign")
    list_select_related = ("service", "assignee")
    date_hierarchy = "created_at"
    list_per_page = 50
    actions = ["take_to_work", "mark_done", "mark_lost"]
    autocomplete_fields = ("assignee",)
    readonly_fields = (
        "created_at", "updated_at", "page_url", "locale", "utm_source", "utm_medium", "utm_campaign",
        "utm_content", "utm_term", "gclid", "yclid", "ym_client_id", "ip", "user_agent", "consent",
    )
    fieldsets = (
        ("Клиент", {"fields": ("name", "phone", "service", "object_type", "message", "source")}),
        ("Работа с заявкой", {"fields": ("status", "assignee", "next_action_at", "amount", "lost_reason", "new_comment")}),
        (
            "Источник и реклама",
            {
                "classes": ["collapse"],
                "fields": (
                    "page_url", "locale", ("utm_source", "utm_medium"), "utm_campaign", ("utm_content", "utm_term"),
                    "gclid", "yclid", "ym_client_id", "ip", "user_agent", "consent", ("created_at", "updated_at"),
                ),
            },
        ),
    )

    @display(description="№", ordering="id")
    def number(self, obj: Lead) -> str:
        return f"#{obj.pk}"

    @display(description="Этап", ordering="status", label=STATUS_COLORS)
    def show_status(self, obj: Lead):
        return obj.status, obj.get_status_display()

    @display(description="Телефон", ordering="phone")
    def phone_link(self, obj: Lead):
        return format_html(
            '<a href="tel:+{}">{}</a> · <a href="https://wa.me/{}" target="_blank" rel="noopener">WA</a>',
            obj.phone_digits,
            obj.phone,
            obj.phone_digits,
        )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial.setdefault("source", "manual")
        return initial

    def save_model(self, request, obj, form, change):
        obj.save(actor=request.user)
        comment = form.cleaned_data.get("new_comment", "").strip()
        if comment:
            LeadEvent.objects.create(lead=obj, kind=LeadEvent.Kind.COMMENT, text=comment, author=request.user)

    def _bulk(self, request, queryset, status, assign=False):
        for lead in queryset:
            lead.status = status
            if assign and not lead.assignee_id:
                lead.assignee = request.user
            lead.save(actor=request.user)
        self.message_user(request, f"Обновлено заявок: {queryset.count()}", messages.SUCCESS)

    @admin.action(description="Взять в работу (назначить на меня)")
    def take_to_work(self, request, queryset):
        for lead in queryset:
            lead.assignee = request.user
            if lead.status == LeadStatus.NEW:
                lead.status = LeadStatus.IN_WORK
            lead.save(actor=request.user)
        self.message_user(request, f"Назначено на вас: {queryset.count()}", messages.SUCCESS)

    @admin.action(description="Отметить: Завершена")
    def mark_done(self, request, queryset):
        self._bulk(request, queryset, LeadStatus.DONE, assign=True)

    @admin.action(description="Отметить: Отказ")
    def mark_lost(self, request, queryset):
        self._bulk(request, queryset, LeadStatus.LOST)


@admin.register(LeadEvent)
class LeadEventAdmin(ModelAdmin):
    list_display = ("created_at", "lead", "kind", "text", "author")
    list_filter = ("kind", "author", "created_at")
    search_fields = ("text", "lead__phone", "lead__name")
    list_select_related = ("lead", "author")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# --- Сотрудники ---------------------------------------------------------------

admin.site.unregister(User)
admin.site.unregister(Group)


class StaffProfileInline(StackedInline):
    model = StaffProfile
    can_delete = False
    fields = ("link_code", "telegram_username", "telegram_id")
    readonly_fields = ("link_code", "telegram_username", "telegram_id")
    verbose_name_plural = "Telegram"
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    inlines = [StaffProfileInline]
    list_display = ("username", "first_name", "last_name", "email", "is_staff", "is_superuser", "telegram")

    @display(description="Telegram")
    def telegram(self, obj):
        profile = getattr(obj, "staff_profile", None)
        return f"@{profile.telegram_username}" if profile and profile.telegram_username else "—"


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
