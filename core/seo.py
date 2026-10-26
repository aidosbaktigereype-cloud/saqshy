"""Микроразметка Schema.org (JSON-LD) для поисковиков."""

from django.conf import settings


def absolute(path: str) -> str:
    return settings.SITE_URL + path


def local_business() -> dict:
    brand = settings.BRAND
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": absolute("/#business"),
        "name": brand["name"],
        "url": absolute("/"),
        "telephone": brand["phone"],
        "email": brand["email"],
        "image": absolute("/static/img/og.png"),
        "priceRange": "₸₸",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": brand["city"],
            "streetAddress": brand["address"],
            "addressCountry": "KZ",
        },
        "areaServed": {"@type": "City", "name": "Almaty"},
    }
    same_as = [f"https://t.me/{brand['telegram']}"]
    if brand.get("instagram"):
        same_as.append(f"https://instagram.com/{brand['instagram']}")
    data["sameAs"] = same_as
    return data


def breadcrumbs(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": absolute(url)}
            for i, (name, url) in enumerate(items, start=1)
        ],
    }


def faq_page(faqs) -> dict | None:
    faqs = list(faqs)
    if not faqs:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f.question, "acceptedAnswer": {"@type": "Answer", "text": f.answer}}
            for f in faqs
        ],
    }


def service(service_obj) -> dict:
    data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service_obj.h1,
        "description": service_obj.seo_description or service_obj.summary,
        "provider": {"@id": absolute("/#business")},
        "areaServed": {"@type": "City", "name": "Almaty"},
        "url": absolute(service_obj.get_absolute_url()),
    }
    if service_obj.price_from:
        data["offers"] = {
            "@type": "Offer",
            "priceCurrency": "KZT",
            "price": service_obj.price_from,
            "priceSpecification": {"@type": "PriceSpecification", "minPrice": service_obj.price_from, "priceCurrency": "KZT"},
        }
    return data
