import requests
import re

# Banner
print("\033[91m")
print("###############################################")
print("#        Sheikh's Expanded DNS Scraper         #")
print("###############################################")
print("\033[0m")

# Function to extract valid IPs from text
def extract_ips(text):
    # Regex pattern to match IPv4 addresses
    ip_pattern = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")
    return ip_pattern.findall(text)

# Scrape DNS servers from a comprehensive list of DNS-only sources
def scrape_dns_servers():
    sources = [
        "https://public-dns.info/nameservers-all.txt",        # Source 1: Public DNS
        "https://www.dnsserverlist.org/",
    ]
    
    dns_servers = set()  # Use set to avoid duplicates

    for url in sources:
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            ips = extract_ips(response.text)
            dns_servers.update(ips)
            print(f"Found {len(ips)} DNS servers from {url}")
        except Exception as e:
            print(f"Error fetching DNS servers from {url}: {e}")

    print(f"Total unique DNS servers found: {len(dns_servers)}")
    return list(dns_servers)

# Function to save DNS servers to a text file
def save_dns_servers(dns_servers, file_path):
    try:
        with open(file_path, 'w') as f:
            for server in dns_servers:
                f.write(server + '\n')
        print(f"Saved {len(dns_servers)} DNS servers to {file_path}.")
    except Exception as e:
        print(f"Error saving DNS servers: {e}")

if __name__ == "__main__":
    # Scrape DNS servers from the expanded sources
    dns_servers = scrape_dns_servers()

    if dns_servers:
        # Save to a text file
        file_path = input("Enter the file path to save DNS servers: ")
        save_dns_servers(dns_servers, file_path)
    else:
        print("No DNS servers found. Exiting.")
