import bleach


ALLOWED_TAGS = set(bleach.sanitizer.ALLOWED_TAGS).union(
    {"h1", "h2", "h3", "p", "br", "ul", "ol", "li", "blockquote"}
)
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
}
ALLOWED_PROTOCOLS = {"http", "https", "mailto"}


def clean_rich_text(value: str) -> str:
    """Remove unsafe markup while preserving approved task formatting."""
    return bleach.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
