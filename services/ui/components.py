import html
import streamlit as st

BAD_WORDS = ("low", "shallow", "bad", "incorrect", "swing", "arch", "sag", "pike",
             "unstable", "too", "poor", "not", "bent", "forward", "lean", "uneven")
GOOD_WORDS = ("good", "ok", "correct", "perfect", "stable", "straight", "full",
              "aligned", "proper", "deep", "parallel", "balanced", "locked")


def _render(markup: str):
    st.markdown(markup, unsafe_allow_html=True)


def _tone(value) -> str:
    """Pick a colour for a status text. Adjust the word lists to your own status strings."""
    v = str(value).strip().lower()
    if v in ("", "n/a", "--") or v.endswith("°"):
        return ""
    if any(w in v for w in BAD_WORDS):
        return "bad"
    if any(w in v for w in GOOD_WORDS):
        return "good"
    return "warn"


def hero(title: str, subtitle: str, live: bool = False):
    pill = (
        '<span class="pill live"><span class="dot"></span>LIVE SESSION</span>'
        if live else
        '<span class="pill"><span class="dot"></span>READY</span>'
    )
    _render(
        f'{pill}<div class="hero-title">{html.escape(title)}</div>'
        f'<div class="hero-sub">{html.escape(subtitle)}</div>'
    )


def brand(username: str | None):
    user = f'@{html.escape(str(username))}' if username else ""
    _render(
        '<div class="brand"><div class="brand-logo">🏋️</div>'
        f'<div><div class="brand-name">APNA AI COACH</div><div class="brand-user">{user}</div></div></div>'
    )


def section_label(text: str):
    _render(f'<div class="section-label">{html.escape(text)}</div>')


def plan_chip(exercise, sets, reps):
    _render(
        f'<div class="plan-chip"><b>{html.escape(str(exercise))}</b>'
        f'<span>{sets} sets × {reps} reps</span></div>'
    )


def stat_card(label: str, value, tone: str | None = None):
    tone = _tone(value) if tone is None else tone
    return (
        f'<div class="stat {tone}"><span class="stat-label">{html.escape(label)}</span>'
        f'<span class="stat-value">{html.escape(str(value))}</span></div>'
    )


def stat_cards(items):
    """items: list of (label, value)."""
    _render("".join(stat_card(label, value) for label, value in items))


def _ring(current, total, label):
    pct = 0 if not total else max(0, min(100, current / total * 100))
    return (
        '<div class="ring-wrap">'
        f'<div class="ring" style="--p:{pct:.0f}"><div class="ring-inner">'
        f'<span class="ring-val">{current}/{total}</span></div></div>'
        f'<div class="ring-label">{html.escape(label)}</div></div>'
    )


def progress_rings(current_set_reps, reps_per_set, sets_completed, target_sets):
    _render(
        '<div class="rings">'
        + _ring(current_set_reps or 0, reps_per_set or 0, "Current set")
        + _ring(sets_completed or 0, target_sets or 0, "Sets done")
        + "</div>"
    )


def coach_bubble(text: str):
    _render(
        '<div class="coach"><div class="coach-avatar">🤖</div><div>'
        '<div class="coach-name">COACH</div>'
        f'<div class="coach-text">{html.escape(str(text))}</div></div></div>'
    )


def empty_state():
    steps = [
        ("🎯", "Pick exercise", "Squats, push-ups, curls, press or lunges."),
        ("🔢", "Set sets & reps", "Decide your target in the sidebar."),
        ("🚀", "Hit Start", "Camera + AI voice coach go live."),
    ]
    cards = "".join(
        f'<div class="step"><div class="step-num">{i}</div><div class="step-icon">{icon}</div>'
        f'<b>{title}</b><span>{desc}</span></div>'
        for i, (icon, title, desc) in enumerate(steps, 1)
    )
    _render(f'<div class="steps">{cards}</div>')


def kpi_grid(items):
    """items: list of (value, label)."""
    cells = "".join(
        f'<div class="kpi"><div class="kpi-val">{html.escape(str(v))}</div>'
        f'<div class="kpi-label">{html.escape(l)}</div></div>'
        for v, l in items
    )
    _render(f'<div class="kpi-grid">{cells}</div>')


def login_hero():
    _render(
        '<div class="login-hero"><div class="login-logo">🏋️</div>'
        '<div class="hero-title">AI Real-time<br>Gym Trainer</div>'
        '<div class="hero-sub">Pose detection + live voice coaching. Enter a username to begin.</div>'
        '<div class="chips"><span class="chip">📷 Live pose tracking</span>'
        '<span class="chip">🎙️ AI voice coach</span>'
        '<span class="chip">📈 Progress history</span></div></div>'
    )