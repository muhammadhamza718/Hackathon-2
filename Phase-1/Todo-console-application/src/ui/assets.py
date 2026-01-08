"""
Visual assets for the Premium Todo TUI application.

Contains ASCII art generators and visual elements for the "Cyberpunk/Neon" aesthetic.
"""

from rich.text import Text
from rich.console import Console
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static


def generate_todo_ascii_art() -> str:
    """
    Generate ASCII art for the "TODO" text.

    Returns:
        str: ASCII art representation of "TODO"
    """
    # Bold, Blocky ASCII art for TODO
    ascii_art = r"""
████████╗ ██████╗ ██████╗  ██████╗ 
╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗
   ██║   ██║   ██║██║  ██║██║   ██║
   ██║   ██║   ██║██║  ██║██║   ██║
   ██║   ╚██████╔╝██████╔╝╚██████╔╝
   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ 
    """
    return ascii_art


def create_gradient_todo_logo() -> Text:
    """
    Create a gradient-styled "TODO" logo using Rich text.

    Returns:
        Text: Rich Text object with gradient styling
    """
    # Create the text using the bold ASCII art
    logo_content = generate_todo_ascii_art()
    logo_text = Text(logo_content, style="bold")

    # Apply gradient colors - Cyberpunk style (Neon Cyan to Neon Pink)
    colors = ["#00f3ff", "#00f3ff", "#bc13fe", "#ff00ff"]
    
    # We'll just gradient the whole block for simplicity or iterate lines
    # Let's try to map colors to lines for a vertical gradient effect
    lines = logo_content.split('\n')
    line_colors = ["#00f3ff", "#40c4ff", "#8095ff", "#bf66ff", "#ff36ff", "#ff00ff"]
    
    # Reconstruct as a text object with gradients per line
    styled_logo = Text()
    for i, line in enumerate(lines):
        if i < len(line_colors):
            color = line_colors[i]
        else:
            color = line_colors[-1]
            
        styled_logo.append(line + "\n", style=f"bold {color}")
        
    return styled_logo


class HeaderWidget(Widget):
    """Header widget displaying the TODO logo."""

    def compose(self) -> ComposeResult:
        """Compose the header widget."""
        yield Static(create_gradient_todo_logo(), id="header-logo")