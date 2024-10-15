import requests
import argparse
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor


def print_banner():
    banner = """
                     +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+
                     |S|h|e|i|k|h|s| |P|a|t|h|f|i|n|d|e|r|
                     +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+
    """
    print(colored(banner, "cyan"))


def load_paths_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            paths = [line.strip() for line in file if line.strip()]
        return paths
    except FileNotFoundError:
        print(colored(f"[ERROR] The file '{file_path}' was not found.", "red"))
        return []


def check_path(base_url, path, found_paths):
    full_url = base_url + path
    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            print(colored(f"[FOUND] {full_url} - Status: {response.status_code}", "green"))
            found_paths.append(full_url)
        else:
            print(colored(f"[NOT FOUND] {full_url} - Status: {response.status_code}", "red"))
    except requests.ConnectionError:
        print(colored(f"[ERROR] Could not connect to {full_url}", "red"))


def find_paths(base_url, paths, threads):
    if not base_url.startswith("http"):
        base_url = "http://" + base_url

    print(f"Starting Sheikh's Pathfinder on {base_url}\n")
    found_paths = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_path, base_url, path, found_paths) for path in paths]
        for future in futures:
            future.result()

    
    if found_paths:
        with open("pathsfound.txt", "w") as f:
            for path in found_paths:
                f.write(path + "\n")
        print(colored(f"\n[INFO] Found paths saved to 'pathsfound.txt'", "cyan"))


if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description="Sheikh's Pathfinder - URL Path Finder with Threads")
    parser.add_argument("url", help="The base URL to search paths on.")
    parser.add_argument("--file", help="Path to a text file containing custom paths to check.")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads to use for checking paths.")
    args = parser.parse_args()

    if args.file:
        paths = load_paths_from_file(args.file)
    else:
        paths = [
            "/admin", "/login", "/wp-admin", "/robots.txt", "/config.php", "/.git", "/.htaccess",
            "/phpmyadmin", "/sitemap.xml", "/upload", "/images", "/backup", "/test", "/wp-login.php",
            "/shell.php", "/cmd.php", "/index.php", "/api", "/debug", "/logs", "/server-status",
            "/admin/login", "/admin/panel", "/admin/dashboard", "/panel","/controlpanel", "/cpanel", "/db", "/data", "/settings", "/config.json", "/api/v1",
            "/manage", "/admin/config", "/cgi-bin", "/cgi", "/admin/cmd", "/server", "/admin/shell",
            "/uploads", "/files", "/admin/api", "/admin/upload", "/system"
        ]

    if paths:
        find_paths(args.url, paths, args.threads)
