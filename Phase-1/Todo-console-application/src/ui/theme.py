"""
Theme configuration for the Premium Todo TUI application.

Defines the "Cyberpunk/Neon" style color palette and visual styling.
"""

# Color palette - Cyberpunk Neon
BACKGROUND = "#050510"  # Void Black
FOREGROUND = "#e0e0e0"  # Off-white

# High contrast neons
ACCENT_PRIMARY = "#00f3ff"  # Cyan Neon
ACCENT_SECONDARY = "#ff00ff"  # Magenta Neon
ACCENT_TERTIARY = "#39ff14"  # Neon Green

# UI Architecture colors
HEADER_BG = "#0a0a1a"
SIDEBAR_BG = "#080814"
CONTENT_BG = "#050510"
BORDER_COLOR = "#2a2a40"  # Dark blue-grey border
HIGHLIGHT_COLOR = "#ff0099"  # Hot pink highlight

# Status colors
STATUS_COMPLETED = "#39ff14"  # Neon Green
STATUS_PENDING = "#ff3300"    # Neon Red/Orange
STATUS_OVERDUE = "#ff0055"    # Crimson

# Text colors
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#b0b0d0"
TEXT_MUTED = "#505070"

# Button and interaction colors
BUTTON_PRIMARY = "#7000ff"    # Electric Purple
BUTTON_PRIMARY_HOVER = "#9d40ff"
BUTTON_DANGER = "#ff0033"
BUTTON_DANGER_HOVER = "#ff4d70"

# Success and error colors
SUCCESS_COLOR = "#00ff9d" # Mint Green
ERROR_COLOR = "#ff0055"
WARNING_COLOR = "#ffcc00"

# Theme configuration dictionary
THEME_CONFIG = {
    "background": BACKGROUND,
    "foreground": FOREGROUND,
    "accent_primary": ACCENT_PRIMARY,
    "accent_secondary": ACCENT_SECONDARY,
    "header_bg": HEADER_BG,
    "sidebar_bg": SIDEBAR_BG,
    "content_bg": CONTENT_BG,
    "border_color": BORDER_COLOR,
    "highlight_color": HIGHLIGHT_COLOR,
    "status_completed": STATUS_COMPLETED,
    "status_pending": STATUS_PENDING,
    "status_overdue": STATUS_OVERDUE,
    "text_primary": TEXT_PRIMARY,
    "text_secondary": TEXT_SECONDARY,
    "text_muted": TEXT_MUTED,
    "button_primary": BUTTON_PRIMARY,
    "button_primary_hover": BUTTON_PRIMARY_HOVER,
    "button_danger": BUTTON_DANGER,
    "button_danger_hover": BUTTON_DANGER_HOVER,
    "success_color": SUCCESS_COLOR,
    "error_color": ERROR_COLOR,
    "warning_color": WARNING_COLOR,
}

# CSS theme string for Textual
THEME_CSS = f"""
/* Background and general styling */
Screen {{
    background: {BACKGROUND};
    color: {TEXT_PRIMARY};
}}

/* Header styling */
Header {{
    background: {HEADER_BG};
    color: {ACCENT_PRIMARY};
    border-bottom: heavy {ACCENT_SECONDARY};
    height: 3;
    content-align: center middle;
    text-style: bold;
}}

/* Sidebar styling */
Sidebar {{
    background: {SIDEBAR_BG};
    color: {TEXT_SECONDARY};
    border-right: heavy {BORDER_COLOR};
    width: 28;
}}

.section-title {{
    background: {HEADER_BG};
    color: {ACCENT_PRIMARY};
    padding: 1;
    text-align: center;
    text-style: bold;
    border-bottom: solid {BORDER_COLOR};
    border-top: solid {BORDER_COLOR};
}}

/* Main content area */
Content {{
    background: {CONTENT_BG};
    color: {TEXT_PRIMARY};
    padding: 1;
}}

/* DataTable styling */
DataTable {{
    background: {CONTENT_BG};
    color: {TEXT_PRIMARY};
    border: solid {BORDER_COLOR};
}}

DataTable > .datatable--header {{
    background: {HEADER_BG};
    color: {ACCENT_PRIMARY};
    text-style: bold;
    border-bottom: double {ACCENT_SECONDARY};
}}

DataTable > .datatable--odd-row {{
    background: {CONTENT_BG};
}}

DataTable > .datatable--even-row {{
    background: {SIDEBAR_BG};
}}

DataTable > .datatable--cursor {{
    background: {BUTTON_PRIMARY};
    color: {TEXT_PRIMARY};
    text-style: bold;
}}

/* Input styling */
Input {{
    background: {SIDEBAR_BG};
    color: {ACCENT_PRIMARY};
    border: solid {BORDER_COLOR};
    width: 100%;
}}

Input:focus {{
    border: heavy {ACCENT_PRIMARY};
    background: {BACKGROUND};
}}

/* Button styling */
Button {{
    background: {BUTTON_PRIMARY};
    color: white;
    border: none;
    height: 3; 
    min-width: 16;
}}

Button:hover {{
    background: {BUTTON_PRIMARY_HOVER};
    border-bottom: heavy {ACCENT_PRIMARY};
}}

Button.-error {{
    background: {BUTTON_DANGER};
}}

Button.-error:hover {{
    background: {BUTTON_DANGER_HOVER};
}}

/* Status indicators */
.status-completed {{
    color: {STATUS_COMPLETED};
    text-style: bold;
}}

.status-pending {{
    color: {STATUS_PENDING};
    text-style: italic;
}}

/* Scrollbar styling */
ScrollableContainer > .scrollbar-background {{
    background: {SIDEBAR_BG};
}}

ScrollableContainer > .scrollbar-thumb {{
    background: {BORDER_COLOR};
}}

ScrollableContainer > .scrollbar-thumb:hover {{
    background: {ACCENT_PRIMARY};
}}

/* Specific IDs */
#sidebar-logo {{
    height: 8;
    content-align: center middle;
    color: {ACCENT_SECONDARY};
    text-style: bold;
    border-bottom: heavy {BORDER_COLOR};
    padding-bottom: 1;
}}

#stats {{
    background: {SIDEBAR_BG};
    border: solid {BORDER_COLOR};
    padding: 1;
    margin: 1;
    color: {ACCENT_TERTIARY};
}}

#status-filter-controls {{
    height: auto;
    align: center middle;
    margin-bottom: 1;
}}

#search-container {{
    height: auto;
    margin-bottom: 1;
    border-bottom: solid {BORDER_COLOR};
    padding-bottom: 1;
}}

#status-bar {{
    height: 3;
    background: {HEADER_BG};
    color: {TEXT_MUTED};
    border-top: heavy {ACCENT_SECONDARY};
    content-align: center middle;
}}
"""