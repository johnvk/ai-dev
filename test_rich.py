from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

console = Console()

# Colored text
console.print("Hello [bold green]John![/bold green] Welcome to AI development 🚀")

# Panel
console.print(Panel("This is a nice panel", title="Session 2", style="cyan"))

# Different styles
console.print("[bold red]URGENT[/bold red] - App is down!")
console.print("[bold yellow]NORMAL[/bold yellow] - Password reset request")
console.print("[bold green]LOW[/bold green] - Update email address")