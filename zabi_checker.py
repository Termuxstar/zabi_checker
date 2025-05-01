#!/usr/bin/env python3

import requests
import socket
import whois
from urllib.parse import urlparse
import os

# === Insert your actual Google API key below ===
API_KEY = "YOUR GOOGLE API KEY"

def show_banner():
    print("""
\033[1;35m+-----------------------------+
|     Created by Zabiullah     |
+-----------------------------+\033[0m
    """)

def check_google_safe_browsing(url):
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
    payload = {
        "client": {"clientId": "zabi_checker", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    try:
        res = requests.post(api_url, json=payload)
        result = res.json()
        return result.get("matches") is not None
    except Exception as e:
        print(f"\033[1;33m[Error] Google API: {e}\033[0m")
        return False

def is_phishing_url(url):
    try:
        response = requests.get(url, timeout=5)
        keywords = ["login", "verify", "password", "bank", "update"]
        return any(word in response.text.lower() for word in keywords)
    except:
        return False

def get_ip(url):
    try:
        hostname = urlparse(url).netloc
        return socket.gethostbyname(hostname)
    except:
        return "\033[1;31m[Error] Could not resolve IP\033[0m"

def check_whois(url):
    try:
        domain = urlparse(url).netloc
        w = whois.whois(domain)
        return str(w.domain_name), str(w.creation_date)
    except:
        return "\033[1;31m[Error] WHOIS lookup failed\033[0m"

def main():
    while True:
        os.system("clear")
        show_banner()
        url = input("\033[1;34m\nEnter a URL to scan (or type 'exit' to quit): \033[0m").strip()
        if url.lower() == "exit":
            print("\033[1;35mExiting Zabi Checker...\033[0m")
            break

        print(f"\033[1;36m\n[+] Checking URL: {url}\033[0m")

        google_check = check_google_safe_browsing(url)
        phishing_check = is_phishing_url(url)

        # Checking Google Safe Browsing Status
        if google_check:
            print("\033[1;32m[+] Google Safe Browsing: URL is Clean.\033[0m")
        else:
            print("\033[1;31m[!] Google Safe Browsing: URL is Unsafe!\033[0m")

        # Checking Phishing Status
        if phishing_check:
            print("\033[1;31m[!] Local Check: Phishing Pattern Detected!\033[0m")
        else:
            print("\033[1;32m[+] Local Check: No Phishing Pattern Found.\033[0m")

        # Overall status based on checks
        if google_check and not phishing_check:
            print("\033[1;32m[+] URL is Safe! (Green)\033[0m")
            data_leak_message = "\033[1;32m[+] Your data is not being leaked. The data remains with the data owner.\033[0m"
        else:
            print("\033[1;31m[!] URL is Unsafe! (Red)\033[0m")
            data_leak_message = "\033[1;31m[!] Data Leak Possible. Please be cautious!\033[0m"

        # Print IP address and WHOIS info
        ip = get_ip(url)
        print(f"\033[1;33m[+] IP Address: {ip}\033[0m")

        domain_info = check_whois(url)
        print(f"\033[1;33m[+] Domain Info: {domain_info}\033[0m")

        # Data safety disclaimer
        print(f"\033[1;35m{data_leak_message}\033[0m")

        input("\033[1;34m\nPress Enter to scan another URL...\033[0m")

if __name__ == "__main__":
    main()
