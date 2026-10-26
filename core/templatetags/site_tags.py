import json

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

# Иконки 24×24 в линейном стиле (stroke = currentColor).
ICONS = {
    "hub": '<rect x="4" y="4" width="16" height="16" rx="4"/><circle cx="12" cy="12" r="2.5"/><path d="M8 4V2.5M16 4V2.5"/>',
    "camera": '<path d="M3 7.5 15.5 4l2 6L5 13.5z"/><path d="M15.5 10.5 21 9v5l-4.6 1.3"/><path d="M8 13v4H4.5M4.5 15v4"/>',
    "access": '<rect x="6" y="3" width="12" height="18" rx="2.5"/><circle cx="12" cy="9.5" r="2.5"/><path d="M9 15.5h6M10 18h4"/>',
    "alarm": '<path d="M6 17V11a6 6 0 0 1 12 0v6"/><path d="M4 17h16v3H4z"/><path d="M12 2v2M4.2 5.2l1.4 1.4M19.8 5.2l-1.4 1.4"/>',
    "network": '<rect x="9" y="3" width="6" height="5" rx="1"/><rect x="3" y="16" width="6" height="5" rx="1"/><rect x="15" y="16" width="6" height="5" rx="1"/><path d="M12 8v4M6 16v-4h12v4"/>',
    "shield": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "phone": '<path d="M5 4h3.5l1.5 4-2 1.5a11 11 0 0 0 6.5 6.5L16 14l4 1.5V19a1.5 1.5 0 0 1-1.6 1.5A15.5 15.5 0 0 1 3.5 5.6 1.5 1.5 0 0 1 5 4z"/>',
    "whatsapp": '<path d="M4 20l1.2-3.9A8.5 8.5 0 1 1 8.6 19z"/><path d="M9.2 8.5c.2-.5.5-.5.8-.5h.5l1 2.2-.7.9a5.6 5.6 0 0 0 2.6 2.6l.9-.7 2.2 1v.5c0 .3 0 .6-.5.8-1.6.9-6.5-1.6-6.8-6.8z"/>',
    "telegram": '<path d="M21 4.5 3 11.6l5.5 2 2 6 3.2-3.6 4.8 3.5z"/><path d="m8.5 13.6 9-6.6-7 7.6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "pin": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 6 8-6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "ruler": '<path d="M3.5 16.5 16.5 3.5l4 4-13 13z"/><path d="m7 13 1.5 1.5M10 10l1.5 1.5M13 7l1.5 1.5"/>',
    "file": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M9.5 12h6M9.5 15.5h6"/>',
    "wrench": '<path d="M14.5 5.5a4 4 0 0 0 5 5L11 19a2.1 2.1 0 0 1-3-3l8.5-8.5"/><path d="M14.5 5.5 17 3"/>',
    "smartphone": '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.5h2"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.4 2.6 3.5 5.4 3.5 8.5s-1.1 5.9-3.5 8.5c-2.4-2.6-3.5-5.4-3.5-8.5S9.6 6.1 12 3.5z"/>',
    "home": '<path d="m4 11 8-6.5 8 6.5"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>',
    "building": '<rect x="5" y="3.5" width="14" height="17" rx="1"/><path d="M9 7.5h2M13 7.5h2M9 11h2M13 11h2M9 14.5h2M13 14.5h2M10.5 20.5v-3h3v3"/>',
    "store": '<path d="M4 9.5 5.5 4h13L20 9.5"/><path d="M4 9.5a2.7 2.7 0 0 0 5.3 0 2.7 2.7 0 0 0 5.4 0 2.7 2.7 0 0 0 5.3 0"/><path d="M5.5 11.5V20h13v-8.5M10 20v-4.5h4V20"/>',
    "warehouse": '<path d="M3 20V9l9-5 9 5v11"/><path d="M7 20v-7h10v7M7 16h10"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>',
}


@register.simple_tag
def icon(name: str, cls: str = "icon", size: int = 24):
    body = ICONS.get(name, ICONS["shield"])
    return format_html(
        '<svg class="{}" width="{}" height="{}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>',
        cls,
        size,
        size,
        mark_safe(body),
    )


@register.filter
def money(value) -> str:
    """290000 → «290 000» (неразрывные пробелы)."""
    try:
        return f"{int(value):,}".replace(",", " ")
    except (TypeError, ValueError):
        return ""


@register.filter
def jsonld(value) -> str:
    text = json.dumps(value, ensure_ascii=False).replace("</", "<\\/")
    return mark_safe(text)
