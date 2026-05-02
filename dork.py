import shodan
import configparser
from colorama import Fore, Style
import argparse
import sys
import os
from sys import stdout

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    clear()
    stdout.write("                                                                                         \n")
    stdout.write("" + Fore.LIGHTRED_EX + "███████╗██╗  ██╗ ██╗██████╗ ██████╗  ██████╗ ██╗    ██╗███████╗\n")
    stdout.write("" + Fore.LIGHTRED_EX + "██╔════╝██║ ██╔╝███║██╔══██╗██╔══██╗██╔═████╗██║    ██║╚══███╔╝\n")
    stdout.write("" + Fore.LIGHTRED_EX + "███████╗█████╔╝ ╚██║██║  ██║██████╔╝██║██╔██║██║ █╗ ██║  ███╔╝ \n")
    stdout.write("" + Fore.LIGHTRED_EX + "╚════██║██╔═██╗  ██║██║  ██║██╔══██╗████╔╝██║██║███╗██║ ███╔╝ \n")
    stdout.write("" + Fore.LIGHTRED_EX + "███████║██║  ██╗ ██║██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝███████╗\n")
    stdout.write("" + Fore.LIGHTRED_EX + "╚══════╝╚═╝  ╚═╝ ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝\n")
    stdout.write("" + Fore.YELLOW + "════════════════════════════════════════════════════════════════════════════════════════\n")
    stdout.write("" + Style.BRIGHT + Fore.YELLOW + f"{'Coded by Sk1drowz'.center(80)}\n")
    stdout.write("" + Style.BRIGHT + Fore.YELLOW + f"{'Shodan Scraper Tool (Premium Edition)'.center(80)}\n")
    stdout.write("" + Style.BRIGHT + Fore.YELLOW + f"{'Copyright By: Hamba Abdi'.center(80)}\n")
    stdout.write("" + Fore.YELLOW + "════════════════════════════════════════════════════════════════════════════════════════\n")
    print(f"{Fore.YELLOW}[Install Module First!] - {Fore.GREEN}pip install -r requirements.txt\n")

    parser = argparse.ArgumentParser(description='Shodan Scraper Tool')
    parser.add_argument('-q', '--query', nargs='+', help='Shodan dork query', required=True)
    parser.add_argument('-t', '--total_results', type=int, default=0, help='Total number of results to retrieve (0 to download all)')
    args = parser.parse_args()

    query = " ".join(args.query)
    total_limit = args.total_results
    filename = "target.txt"

    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        shodan_api_key = config['API_KEYS']['SHODAN_API_KEY']
    except KeyError:
        print(f"{Fore.RED}[!] Please ensure config.ini exists and contains SHODAN_API_KEY under [API_KEYS]{Style.RESET_ALL}")
        return

    api = shodan.Shodan(shodan_api_key)

    print(f"[*] Dorking  : {Fore.GREEN}{query}{Style.RESET_ALL}")
    print(f"[*] Fetching data using Premium Cursor...\n")

    count = 0
    try:
        with open(filename, "a") as f:
            for result in api.search_cursor(query):
                ip = result['ip_str']
                port = result['port']
                
                f.write(f"{ip}:{port}\n")
                
                count += 1
                
                sys.stdout.write(f"\r[+] Successfully fetched: {Fore.YELLOW}{count}{Style.RESET_ALL} targets")
                sys.stdout.flush()

                if total_limit > 0 and count >= total_limit:
                    break

        print(f"\n\n{Fore.GREEN}[+] Done! All {count} targets have been temporarily saved to {filename}{Style.RESET_ALL}")

        # --- Interactive Save Prompt ---
        save_choice = input(f"\nDo you want to save IP only (Y) or IP:port combinations (N)? ").strip().lower()

        if save_choice == 'y':
            with open(filename, 'r') as f:
                lines = f.readlines()
            with open(filename, 'w') as f:
                for line in lines:
                    if ':' in line:
                        ip = line.strip().split(':')[0]
                        f.write(f"{ip}\n")
                    else:
                        f.write(line)
            print(f"{Fore.GREEN}[+] Saved only IPs to {filename}{Style.RESET_ALL}")
        elif save_choice == 'n':
            print(f"{Fore.GREEN}[+] Saved IPs with ports to {filename}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Invalid choice. Saved IPs with ports (default) to {filename}{Style.RESET_ALL}")

    except shodan.APIError as e:
        print(f"\n{Fore.RED}[!] Shodan API Error: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Unexpected Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()