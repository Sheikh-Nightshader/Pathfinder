import requests
import re

# Banner
print("\033[91m")
print("###############################################")
print("#        Sheikh's Enhanced DNS Scraper        #")
print("###############################################")
print("\033[0m")

# Function to extract valid IPv4 DNS server IPs from the response text
def extract_ips(text):
    ip_pattern = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")
    return ip_pattern.findall(text)

# Scrape DNS servers from a comprehensive list of reliable DNS server sources
def scrape_dns_servers():
    sources = [
        # Original sources
        "https://public-dns.info/nameservers-all.txt",        # Public DNS
        "https://www.dnsserverlist.org/",                     # DNS Server List
        "https://dnschecker.org/public-dns.php",              # DNS Checker
        "https://raw.githubusercontent.com/merbanan/public-dns-server/master/list.txt", # GitHub Public DNS
        "https://www.opennic.org/",                           # OpenNIC DNS
        "https://developers.google.com/speed/public-dns/docs/using",  # Google Public DNS
        "https://adguard.com/en/adguard-dns/overview.html",   # AdGuard DNS
        "https://dns.watch/",                                 # DNS.Watch Public Servers
        "https://cleanbrowsing.org/",                         # CleanBrowsing DNS
        "https://www.quad9.net/",                             # Quad9 DNS
        # Additional new sources
        "https://www.dnsperf.com/dns-resolver",               # DNSPerf DNS
        "https://www.freenom.world/en/freenom-dns.html",      # Freenom World
        "https://www.iblocklist.com/lists.php",               # IBlockList DNS Servers
        "https://root-servers.org/",                          # Root DNS Servers
        "https://www.verisign.com/en_US/security-services/public-dns/index.xhtml",  # Verisign Public DNS
        "https://www.tiarap.org/",                            # Tiara Public DNS
        "https://ns1.openresolverproject.org/",               # Open Resolver Project DNS
        "https://publicdns.xyz/",                             # PublicDNS.xyz
        "https://www.dnsflagday.net/public-dns-servers/",     # DNS Flag Day List
        "https://zundel.com/public-dns/",                     # Zundel Public DNS
        "https://freefastdns.com/public-dns",                 # Free Fast DNS Servers
        "https://www.ultradns.com/",                          # UltraDNS Public DNS
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
