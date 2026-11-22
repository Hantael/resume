#!/usr/bin/env python3
"""Generate a modern, responsive GitHub Pages site from Marine_Morard_CV.yaml and RenderCV outputs."""

from __future__ import annotations

from datetime import date
import html as html_lib
from pathlib import Path
import re
import shutil
from typing import Any

from ruamel.yaml import YAML

YAML_SOURCE = Path("Marine_Morard_CV.yaml")
OUTPUT_DIR = Path("rendercv_output")
PUBLIC_DIR = Path("public")
PDF_SOURCE = OUTPUT_DIR / "Marine_Morard_CV.pdf"
PDF_TARGET_NAME = "Marine_Morard_CV.pdf"

FRENCH_MONTHS = [
    "",
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre",
]

SOCIAL_URLS = {
    "LinkedIn": "https://linkedin.com/in/{username}",
    "GitHub": "https://github.com/{username}",
    "GitLab": "https://gitlab.com/{username}",
    "X": "https://x.com/{username}",
}

ICONS = {
    "location": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "email": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>',
    "phone": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "linkedin": '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>',
    "github": '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/></svg>',
    "link": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    "download": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>',
    "sun": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>',
    "moon": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>',
    "doc": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>',
    "web": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>',
}


def md_inline(text: Any) -> str:
    """Escape HTML and convert basic inline Markdown (**bold**, *italic*, [label](url))."""
    escaped = html_lib.escape(str(text))
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',
        escaped,
    )
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def format_date_part(value: Any, present_label: str = "Présent") -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, int):
        return str(value)
    text = str(value).strip()
    if text.lower() == "present":
        return present_label
    m = re.fullmatch(r"(\d{4})-(\d{2})(?:-\d{2})?", text)
    if m:
        year, month = int(m.group(1)), int(m.group(2))
        if 1 <= month <= 12:
            return f"{FRENCH_MONTHS[month]} {year}"
    return text


def parse_ym(value: Any, today_ref: date) -> tuple[int, int] | None:
    if value is None or value == "":
        return None
    if isinstance(value, int):
        return (value, 1)
    text = str(value).strip()
    if text.lower() == "present":
        return (today_ref.year, today_ref.month)
    m = re.fullmatch(r"(\d{4})-(\d{2})(?:-\d{2})?", text)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return None


def compute_time_span_fr(start_val: Any, end_val: Any, today_ref: date) -> str:
    start_ym = parse_ym(start_val, today_ref)
    end_ym = parse_ym(end_val, today_ref)
    if not start_ym or not end_ym:
        return ""
    total_months = (end_ym[0] - start_ym[0]) * 12 + (end_ym[1] - start_ym[1]) + 1
    if total_months <= 0:
        return ""
    years, months = divmod(total_months, 12)
    parts: list[str] = []
    if years == 1:
        parts.append("1 an")
    elif years > 1:
        parts.append(f"{years} ans")
    if months >= 1:
        parts.append(f"{months} mois")
    return " ".join(parts)


def format_date_range(
    entry: dict[str, Any],
    present_label: str = "Présent",
    show_time_span: bool = False,
) -> str:
    if entry.get("date") is not None and entry.get("date") != "":
        return format_date_part(entry["date"], present_label)
    start = format_date_part(entry.get("start_date"), present_label)
    end = format_date_part(entry.get("end_date"), present_label)
    if start and end:
        base = f"{start} – {end}"
        if show_time_span:
            span = compute_time_span_fr(
                entry.get("start_date"), entry.get("end_date"), date.today()
            )
            if span:
                return f"{base} ({span})"
        return base
    return start or end


def split_top_level_commas(text: str) -> list[str]:
    """Split a comma-separated skill list while keeping commas inside parentheses intact."""
    cleaned = text.strip().rstrip(".")
    items: list[str] = []
    current: list[str] = []
    depth = 0
    for ch in cleaned:
        if ch == "(":
            depth += 1
            current.append(ch)
        elif ch == ")":
            depth = max(0, depth - 1)
            current.append(ch)
        elif ch == "," and depth == 0:
            token = "".join(current).strip()
            if token:
                items.append(token)
            current = []
        else:
            current.append(ch)
    token = "".join(current).strip()
    if token:
        items.append(token)
    return items


def build_contact_chips(cv: dict[str, Any]) -> str:
    chips: list[str] = []

    if cv.get("location"):
        chips.append(
            f'<span class="chip">{ICONS["location"]}<span>{md_inline(cv["location"])}</span></span>'
        )

    email = cv.get("email")
    if isinstance(email, list):
        emails = email
    elif email:
        emails = [email]
    else:
        emails = []
    for addr in emails:
        safe = html_lib.escape(str(addr))
        chips.append(
            f'<a class="chip chip-link" href="mailto:{safe}">{ICONS["email"]}<span>{safe}</span></a>'
        )

    phone = cv.get("phone")
    if isinstance(phone, list):
        phones = phone
    elif phone:
        phones = [phone]
    else:
        phones = []
    for ph in phones:
        safe = html_lib.escape(str(ph))
        tel_href = re.sub(r"[^+\d]", "", str(ph))
        chips.append(
            f'<a class="chip chip-link" href="tel:{tel_href}">{ICONS["phone"]}<span>{safe}</span></a>'
        )

    website = cv.get("website")
    if isinstance(website, list):
        websites = website
    elif website:
        websites = [website]
    else:
        websites = []
    for site in websites:
        safe = html_lib.escape(str(site))
        label = re.sub(r"^https?://", "", safe).rstrip("/")
        chips.append(
            f'<a class="chip chip-link" href="{safe}" target="_blank" rel="noopener noreferrer">{ICONS["link"]}<span>{label}</span></a>'
        )

    for social in cv.get("social_networks") or []:
        network = str(social.get("network", ""))
        username = str(social.get("username", ""))
        if not network or not username:
            continue
        url = SOCIAL_URLS.get(network, "https://{username}").format(username=username)
        icon = ICONS.get(network.lower(), ICONS["link"])
        chips.append(
            f'<a class="chip chip-link" href="{html_lib.escape(url)}" target="_blank" rel="noopener noreferrer">'
            f'{icon}<span>{html_lib.escape(network)} · {html_lib.escape(username)}</span></a>'
        )

    for conn in cv.get("custom_connections") or []:
        placeholder = str(conn.get("placeholder", ""))
        url = conn.get("url")
        if url:
            chips.append(
                f'<a class="chip chip-link" href="{html_lib.escape(str(url))}" target="_blank" rel="noopener noreferrer">'
                f'{ICONS["link"]}<span>{html_lib.escape(placeholder)}</span></a>'
            )
        elif placeholder:
            chips.append(
                f'<span class="chip">{ICONS["link"]}<span>{html_lib.escape(placeholder)}</span></span>'
            )

    return "\n".join(chips)


def render_experience_section(
    entries: list[dict[str, Any]],
    present_label: str,
    show_time_span: bool = False,
) -> str:
    # Group consecutive roles at the same company into clean company blocks
    groups: list[dict[str, Any]] = []
    for entry in entries:
        company = str(entry.get("company", ""))
        if groups and groups[-1]["company"] == company:
            groups[-1]["roles"].append(entry)
            if not groups[-1]["summary"] and entry.get("summary"):
                groups[-1]["summary"] = entry.get("summary")
        else:
            groups.append(
                {
                    "company": company,
                    "location": str(entry.get("location", "")),
                    "summary": entry.get("summary") or "",
                    "roles": [entry],
                }
            )

    blocks: list[str] = []
    for group in groups:
        summary_html = (
            f'<p class="company-meta">{md_inline(group["summary"])}</p>'
            if group["summary"]
            else ""
        )
        loc_html = (
            f'<span class="company-loc">{md_inline(group["location"])}</span>'
            if group["location"]
            else ""
        )
        roles_html: list[str] = []
        for role in group["roles"]:
            date_str = format_date_range(role, present_label, show_time_span=show_time_span)
            highlights = role.get("highlights") or []
            bullets_html = "".join(
                f"<li>{md_inline(item)}</li>" for item in highlights
            )
            roles_html.append(
                f"""
                <div class="role-item">
                    <div class="role-header">
                        <h3 class="role-title">{md_inline(role.get("position", ""))}</h3>
                        <span class="date-badge">{html_lib.escape(date_str)}</span>
                    </div>
                    <ul class="bullet-list">{bullets_html}</ul>
                </div>
                """
            )

        blocks.append(
            f"""
            <article class="exp-card">
                <div class="company-header">
                    <div>
                        <div class="company-name-row">
                            <span class="company-name">{md_inline(group["company"])}</span>
                            {loc_html}
                        </div>
                        {summary_html}
                    </div>
                </div>
                <div class="roles-stack">
                    {"".join(roles_html)}
                </div>
            </article>
            """
        )
    return f'<div class="timeline">{"".join(blocks)}</div>'


def render_skills_section(entries: list[dict[str, Any]]) -> str:
    cards: list[str] = []
    for entry in entries:
        label = str(entry.get("label", ""))
        details = str(entry.get("details", ""))
        tokens = split_top_level_commas(details)
        pills = "".join(
            f'<span class="skill-pill">{md_inline(token)}</span>' for token in tokens
        )
        cards.append(
            f"""
            <div class="skill-card">
                <h3 class="skill-label">{md_inline(label)}</h3>
                <div class="skill-pills">{pills}</div>
            </div>
            """
        )
    return f'<div class="skills-grid">{"".join(cards)}</div>'


def render_education_section(
    entries: list[dict[str, Any]], present_label: str, degree_template: str
) -> str:
    cards: list[str] = []
    for entry in entries:
        institution = str(entry.get("institution", ""))
        degree = str(entry.get("degree", ""))
        area = str(entry.get("area", ""))
        if degree and area:
            degree_line = degree_template.replace("DEGREE", degree).replace("AREA", area)
        else:
            degree_line = degree or area
        date_str = format_date_range(entry, present_label)
        highlights = entry.get("highlights") or []
        bullets_html = (
            f'<ul class="bullet-list">{"".join(f"<li>{md_inline(h)}</li>" for h in highlights)}</ul>'
            if highlights
            else ""
        )
        cards.append(
            f"""
            <div class="edu-card">
                <div class="role-header">
                    <div>
                        <h3 class="role-title">{md_inline(institution)}</h3>
                        <p class="edu-degree">{md_inline(degree_line)}</p>
                    </div>
                    <span class="date-badge">{html_lib.escape(date_str)}</span>
                </div>
                {bullets_html}
            </div>
            """
        )
    return f'<div class="edu-stack">{"".join(cards)}</div>'


def render_section(
    title: str,
    entries: list[Any],
    present_label: str,
    degree_template: str,
    show_time_span: bool = False,
) -> str:
    if not entries:
        return ""
    first = entries[0]

    if isinstance(first, str):
        paragraphs = "".join(f'<p class="prose-text">{md_inline(item)}</p>' for item in entries)
        body_html = f'<div class="prose-card">{paragraphs}</div>'
    elif isinstance(first, dict) and "company" in first:
        body_html = render_experience_section(entries, present_label, show_time_span=show_time_span)
    elif isinstance(first, dict) and "label" in first and "details" in first:
        body_html = render_skills_section(entries)
    elif isinstance(first, dict) and "institution" in first:
        body_html = render_education_section(entries, present_label, degree_template)
    else:
        items = "".join(
            f"<li>{md_inline(item.get('bullet') or item.get('name') or str(item))}</li>"
            for item in entries
        )
        body_html = f'<div class="prose-card"><ul class="bullet-list">{items}</ul></div>'

    return f"""
    <section class="cv-section">
        <div class="section-heading">
            <h2>{html_lib.escape(title)}</h2>
            <span class="section-line" aria-hidden="true"></span>
        </div>
        {body_html}
    </section>
    """


def build_html(data: dict[str, Any], png_names: list[str]) -> str:
    cv = data.get("cv") or {}
    locale = data.get("locale") or {}
    design = data.get("design") or {}
    show_time_spans_in = set(
        (design.get("sections") or {}).get("show_time_spans_in") or []
    )
    present_label = str(locale.get("present") or "Présent")
    degree_template = str(
        (locale.get("phrases") or {}).get("degree_with_area") or "DEGREE en AREA"
    )

    name = str(cv.get("name") or "CV")
    headline = str(cv.get("headline") or "")
    initials = "".join(part[0].upper() for part in name.split()[:2]) or "CV"

    contact_chips = build_contact_chips(cv)
    sections_html = "\n".join(
        render_section(
            sec_title,
            sec_entries,
            present_label,
            degree_template,
            show_time_span=(
                sec_title.lower().replace(" ", "_") in show_time_spans_in
                or sec_title in show_time_spans_in
            ),
        )
        for sec_title, sec_entries in (cv.get("sections") or {}).items()
    )

    today = date.today()
    updated_str = f"{FRENCH_MONTHS[today.month]} {today.year}"

    png_pages_html = "\n".join(
        f'<img class="pdf-page-img" src="./{html_lib.escape(png)}" alt="Aperçu du CV — Page {idx}" loading="lazy" />'
        for idx, png in enumerate(png_names, start=1)
    )

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{html_lib.escape(name)} — CV</title>
    <meta name="description" content="{html_lib.escape(name)} — {html_lib.escape(headline)}" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
    <script>
        (function() {{
            const saved = localStorage.getItem('cv-theme');
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            const theme = saved || (prefersDark ? 'dark' : 'light');
            document.documentElement.setAttribute('data-theme', theme);
        }})();
    </script>
    <style>
        :root {{
            --bg: #f4f7fb;
            --bg-elevated: #ffffff;
            --bg-subtle: #f1f5f9;
            --border: #e2e8f0;
            --border-strong: #cbd5e1;
            --text: #0f172a;
            --text-secondary: #334155;
            --text-muted: #64748b;
            --accent: #004f90;
            --accent-hover: #003a6b;
            --accent-soft: rgba(0, 79, 144, 0.08);
            --accent-border: rgba(0, 79, 144, 0.2);
            --topbar-bg: rgba(244, 247, 251, 0.82);
            --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.04);
            --shadow-md: 0 10px 30px -12px rgba(15, 23, 42, 0.12);
            --radius: 14px;
            --radius-sm: 8px;
        }}

        [data-theme="dark"] {{
            --bg: #090e1a;
            --bg-elevated: #111827;
            --bg-subtle: #1e293b;
            --border: #1f2937;
            --border-strong: #334155;
            --text: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --accent: #60a5fa;
            --accent-hover: #93c5fd;
            --accent-soft: rgba(96, 165, 250, 0.12);
            --accent-border: rgba(96, 165, 250, 0.28);
            --topbar-bg: rgba(9, 14, 26, 0.82);
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.25);
            --shadow-md: 0 12px 32px -12px rgba(0, 0, 0, 0.55);
        }}

        *, *::before, *::after {{
            box-sizing: border-box;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            margin: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            transition: background-color 0.2s ease, color 0.2s ease;
        }}

        /* Sticky Topbar */
        .topbar {{
            position: sticky;
            top: 0;
            z-index: 50;
            background: var(--topbar-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
        }}

        .topbar-inner {{
            max-width: 920px;
            margin: 0 auto;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
            font-size: 14px;
            color: var(--text);
            text-decoration: none;
        }}

        .brand-avatar {{
            width: 30px;
            height: 30px;
            border-radius: 8px;
            background: var(--accent);
            color: #ffffff;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.04em;
        }}

        [data-theme="dark"] .brand-avatar {{
            color: #090e1a;
        }}

        .topbar-actions {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .view-switcher {{
            display: inline-flex;
            padding: 3px;
            border-radius: 10px;
            background: var(--bg-subtle);
            border: 1px solid var(--border);
        }}

        .view-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 11px;
            border: none;
            border-radius: 7px;
            background: transparent;
            color: var(--text-muted);
            font-family: inherit;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .view-btn.active {{
            background: var(--bg-elevated);
            color: var(--text);
            box-shadow: var(--shadow-sm);
        }}

        .icon-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 34px;
            height: 34px;
            border-radius: 9px;
            border: 1px solid var(--border);
            background: var(--bg-elevated);
            color: var(--text-secondary);
            cursor: pointer;
            transition: border-color 0.15s ease, color 0.15s ease;
        }}

        .icon-btn:hover {{
            border-color: var(--border-strong);
            color: var(--text);
        }}

        .theme-icon-sun {{ display: none; }}
        .theme-icon-moon {{ display: inline-flex; }}
        [data-theme="dark"] .theme-icon-sun {{ display: inline-flex; }}
        [data-theme="dark"] .theme-icon-moon {{ display: none; }}

        .btn-primary {{
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 7px 14px;
            border-radius: 9px;
            background: var(--accent);
            color: #ffffff;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            transition: background-color 0.15s ease, transform 0.15s ease;
        }}

        [data-theme="dark"] .btn-primary {{
            color: #090e1a;
        }}

        .btn-primary:hover {{
            background: var(--accent-hover);
            transform: translateY(-1px);
        }}

        /* Main container */
        .container {{
            max-width: 920px;
            margin: 0 auto;
            padding: 32px 20px 64px;
        }}

        /* Hero Card */
        .hero {{
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 32px 34px;
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent), #0ea5e9);
        }}

        .hero-name {{
            margin: 0;
            font-size: clamp(1.75rem, 3.2vw, 2.35rem);
            font-weight: 700;
            letter-spacing: -0.025em;
            line-height: 1.15;
            color: var(--text);
        }}

        .hero-headline {{
            margin: 8px 0 0;
            font-size: clamp(0.98rem, 1.8vw, 1.12rem);
            font-weight: 500;
            color: var(--accent);
        }}

        .contact-chips {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 20px;
        }}

        .chip {{
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 6px 12px;
            border-radius: 999px;
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            font-size: 13px;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.15s ease;
        }}

        .chip-link:hover {{
            border-color: var(--accent-border);
            background: var(--accent-soft);
            color: var(--accent);
        }}

        /* Sections */
        .cv-section {{
            margin-top: 32px;
        }}

        .section-heading {{
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 16px;
        }}

        .section-heading h2 {{
            margin: 0;
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--accent);
            white-space: nowrap;
        }}

        .section-line {{
            flex: 1;
            height: 1px;
            background: var(--border);
        }}

        /* Prose card (Profil / Centres d'intérêt) */
        .prose-card {{
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 20px 24px;
            box-shadow: var(--shadow-sm);
        }}

        .prose-text {{
            margin: 0;
            font-size: 15px;
            color: var(--text-secondary);
        }}

        .prose-text + .prose-text {{
            margin-top: 10px;
        }}

        /* Experience Timeline */
        .timeline {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .exp-card {{
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 22px 24px;
            box-shadow: var(--shadow-sm);
        }}

        .company-header {{
            padding-bottom: 14px;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }}

        .company-name-row {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .company-name {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text);
        }}

        .company-loc {{
            font-size: 13px;
            color: var(--text-muted);
        }}

        .company-meta {{
            margin: 3px 0 0;
            font-size: 13px;
            color: var(--text-muted);
        }}

        .roles-stack {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .role-item {{
            position: relative;
            padding-left: 16px;
            border-left: 2px solid var(--accent-border);
        }}

        .role-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .role-title {{
            margin: 0;
            font-size: 15px;
            font-weight: 600;
            color: var(--text);
        }}

        .date-badge {{
            font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
            font-size: 12px;
            font-weight: 500;
            color: var(--accent);
            background: var(--accent-soft);
            border: 1px solid var(--accent-border);
            padding: 3px 9px;
            border-radius: 999px;
            white-space: nowrap;
        }}

        .bullet-list {{
            margin: 10px 0 0;
            padding-left: 18px;
            color: var(--text-secondary);
            font-size: 14.5px;
        }}

        .bullet-list li {{
            margin-bottom: 6px;
        }}

        .bullet-list li:last-child {{
            margin-bottom: 0;
        }}

        .bullet-list li::marker {{
            color: var(--accent);
        }}

        /* Skills Grid */
        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
        }}

        .skill-card {{
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 18px 20px;
            box-shadow: var(--shadow-sm);
        }}

        .skill-label {{
            margin: 0 0 10px;
            font-size: 13.5px;
            font-weight: 600;
            color: var(--text);
        }}

        .skill-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .skill-pill {{
            display: inline-block;
            font-size: 12.5px;
            font-weight: 500;
            padding: 4px 10px;
            border-radius: 7px;
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            color: var(--text-secondary);
        }}

        /* Education */
        .edu-stack {{
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}

        .edu-card {{
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 20px 24px;
            box-shadow: var(--shadow-sm);
        }}

        .edu-degree {{
            margin: 3px 0 0;
            font-size: 14px;
            color: var(--text-muted);
        }}

        /* PDF Preview Pane */
        .pdf-view {{
            display: none;
        }}

        .pdf-view.active {{
            display: block;
        }}

        .web-view.hidden {{
            display: none;
        }}

        .pdf-frame-wrap {{
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 20px;
            box-shadow: var(--shadow-md);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
        }}

        .pdf-page-img {{
            width: 100%;
            max-width: 794px;
            height: auto;
            border-radius: 6px;
            border: 1px solid var(--border);
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
            background: #ffffff;
        }}

        .pdf-caption {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            max-width: 794px;
            gap: 12px;
            flex-wrap: wrap;
            font-size: 13px;
            color: var(--text-muted);
        }}

        .pdf-open-link {{
            color: var(--accent);
            font-weight: 600;
            text-decoration: none;
        }}

        .pdf-open-link:hover {{
            text-decoration: underline;
        }}

        /* Footer */
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
            font-size: 12.5px;
            color: var(--text-muted);
        }}

        .footer a {{
            color: var(--accent);
            text-decoration: none;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 720px) {{
            .hero {{
                padding: 24px 20px;
            }}
            .exp-card, .prose-card, .edu-card {{
                padding: 18px 18px;
            }}
            .skills-grid {{
                grid-template-columns: 1fr;
            }}
            .brand-name {{
                display: none;
            }}
        }}

        @media print {{
            .topbar, .pdf-view, .footer {{
                display: none !important;
            }}
            .web-view {{
                display: block !important;
            }}
            body {{
                background: #ffffff;
                color: #000000;
            }}
            .container {{
                padding: 0;
                max-width: none;
            }}
            .hero, .exp-card, .prose-card, .skill-card, .edu-card {{
                box-shadow: none;
                border-color: #cbd5e1;
            }}
        }}
    </style>
</head>
<body>
    <header class="topbar">
        <div class="topbar-inner">
            <a class="brand" href="#top">
                <span class="brand-avatar">{html_lib.escape(initials)}</span>
                <span class="brand-name">{html_lib.escape(name)}</span>
            </a>
            <div class="topbar-actions">
                <div class="view-switcher" role="tablist" aria-label="Mode d'affichage du CV">
                    <button class="view-btn active" type="button" role="tab" aria-selected="true" data-view="web">
                        {ICONS["web"]}<span>Vue Web</span>
                    </button>
                    <button class="view-btn" type="button" role="tab" aria-selected="false" data-view="pdf">
                        {ICONS["doc"]}<span>Aperçu PDF</span>
                    </button>
                </div>
                <button class="icon-btn" id="theme-toggle" type="button" aria-label="Changer de thème clair/sombre" title="Mode clair / sombre">
                    <span class="theme-icon-moon">{ICONS["moon"]}</span>
                    <span class="theme-icon-sun">{ICONS["sun"]}</span>
                </button>
                <a class="btn-primary" href="./{PDF_TARGET_NAME}" download="{PDF_TARGET_NAME}">
                    {ICONS["download"]}<span>Télécharger le PDF</span>
                </a>
            </div>
        </div>
    </header>

    <main id="top" class="container">
        <div class="web-view" id="web-view">
            <section class="hero">
                <h1 class="hero-name">{html_lib.escape(name)}</h1>
                <p class="hero-headline">{md_inline(headline)}</p>
                <div class="contact-chips">
                    {contact_chips}
                </div>
            </section>

            {sections_html}
        </div>

        <div class="pdf-view" id="pdf-view" aria-hidden="true">
            <div class="pdf-frame-wrap">
                <div class="pdf-caption">
                    <span>Aperçu haute définition du PDF A4 généré par RenderCV</span>
                    <a class="pdf-open-link" href="./{PDF_TARGET_NAME}" target="_blank" rel="noopener noreferrer">Ouvrir le PDF dans un nouvel onglet ↗</a>
                </div>
                {png_pages_html}
            </div>
        </div>

        <footer class="footer">
            <span>CV as Code — généré automatiquement via RenderCV &amp; GitHub Actions</span>
            <span>Mise à jour : {html_lib.escape(updated_str)} · <a href="./{PDF_TARGET_NAME}" download="{PDF_TARGET_NAME}">{PDF_TARGET_NAME}</a></span>
        </footer>
    </main>

    <script>
        (function() {{
            const root = document.documentElement;
            const themeBtn = document.getElementById('theme-toggle');
            if (themeBtn) {{
                themeBtn.addEventListener('click', function() {{
                    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
                    root.setAttribute('data-theme', next);
                    localStorage.setItem('cv-theme', next);
                }});
            }}

            const buttons = document.querySelectorAll('.view-btn');
            const webView = document.getElementById('web-view');
            const pdfView = document.getElementById('pdf-view');
            buttons.forEach(function(btn) {{
                btn.addEventListener('click', function() {{
                    const view = btn.getAttribute('data-view');
                    buttons.forEach(function(b) {{
                        const isActive = b === btn;
                        b.classList.toggle('active', isActive);
                        b.setAttribute('aria-selected', String(isActive));
                    }});
                    if (view === 'pdf') {{
                        webView.classList.add('hidden');
                        pdfView.classList.add('active');
                        pdfView.setAttribute('aria-hidden', 'false');
                    }} else {{
                        webView.classList.remove('hidden');
                        pdfView.classList.remove('active');
                        pdfView.setAttribute('aria-hidden', 'true');
                    }}
                }});
            }});
        }})();
    </script>
</body>
</html>
"""


def main() -> None:
    if not YAML_SOURCE.exists():
        raise FileNotFoundError(f"Missing CV YAML source: {YAML_SOURCE}")
    if not PDF_SOURCE.exists():
        raise FileNotFoundError(f"Missing generated PDF: {PDF_SOURCE}")

    yaml = YAML(typ="safe")
    data = yaml.load(YAML_SOURCE.read_text(encoding="utf-8"))

    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copy2(PDF_SOURCE, PUBLIC_DIR / PDF_TARGET_NAME)

    png_files = sorted(OUTPUT_DIR.glob("Marine_Morard_CV_*.png"))
    png_names: list[str] = []
    for png in png_files:
        shutil.copy2(png, PUBLIC_DIR / png.name)
        png_names.append(png.name)

    rendered_html = build_html(data, png_names)
    (PUBLIC_DIR / "index.html").write_text(rendered_html, encoding="utf-8")
    (PUBLIC_DIR / ".nojekyll").write_text("", encoding="utf-8")

    print(
        f"Prepared {PUBLIC_DIR}/index.html, {PUBLIC_DIR}/{PDF_TARGET_NAME}, "
        f"and {len(png_names)} PNG preview page(s)."
    )


if __name__ == "__main__":
    main()
