from colorama import Fore, Style


def display_style(message, colors):
    if colors:
        return f"{Style.BRIGHT}{message}{Style.RESET_ALL}"
    else:
        return message


def display_alert(message, colors):
    if colors:
        return f"{Style.BRIGHT}{Fore.YELLOW}[!]{Style.RESET_ALL} {message}"
    else:
        return f"[!] {message}"


def display_info(message, colors):
    if colors:
        return f"\n{Style.BRIGHT}{Fore.BLUE}[*]{Style.RESET_ALL} {message}\n"
    else:
        return f"\n[*] {message}\n"


def display_positive(message, colors):
    if colors:
        return f"\n{Style.BRIGHT}{Fore.GREEN}[+]{Style.RESET_ALL} {message}"
    else:
        return f"\n[+] {message}"


def display_negative(message, colors):
    if colors:
        return f"{Style.BRIGHT}{Fore.RED}[-]{Style.RESET_ALL} {message}"
    else:
        return f"[-] {message}"
