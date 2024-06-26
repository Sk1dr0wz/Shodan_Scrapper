import shodan
import configparser
from colorama import Fore, Style
import argparse
import os
from sys import stdout

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def perform_search(query, filename, start, api_key, total_results):
    api = shodan.Shodan(api_key)

    try:
        results = api.search(query, page=start // 1000 + 1)
        with open(filename, "a") as f:
            for result in results['matches']:
                ip = result['ip_str']
                port = result['port']
                f.write(f"{ip},{port}\n")

        print(f"{Fore.YELLOW}Query {Fore.WHITE}{start // 1000 + 1} {Fore.GREEN}completed.")

        if start >= total_results:
            return True  
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")

    return False  

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
    stdout.write("" + Style.BRIGHT + Fore.YELLOW + f"{'Shodan Scaper Tool'.center(80)}\n")
    stdout.write("" + Style.BRIGHT + Fore.YELLOW + f"{'Copyright By: Hamba Abdi'.center(80)}\n")
    stdout.write("" + Fore.YELLOW + "════════════════════════════════════════════════════════════════════════════════════════\n")
    print(f"{Fore.YELLOW}[Install Module First!] - {Fore.GREEN}pip install -r requirements.txt\n")

    parser = argparse.ArgumentParser(description='Shodan Scrapper Tool')
    parser.add_argument('-q', '--query', help='Shodan dork query', required=True)
    parser.add_argument('-t', '--total_results', type=int, default=1000, help='Total number of results to retrieve (1000 equal to 1 Query. 1 Query equal to 100 results.)')
    args = parser.parse_args()

    query = args.query
    total_results = args.total_results
    chunk_size = 1000
    num_queries = total_results // chunk_size

    filename = "results.txt"

    config = configparser.ConfigParser()
    config.read('config.ini')
    shodan_api_key = config['API_KEYS']['SHODAN_API_KEY']

    api_keys = [shodan_api_key]

    key_index = 0

    for i in range(num_queries):
        start_index = i * chunk_size
        stop_scraping = perform_search(query, filename, start_index, api_keys[key_index], total_results)

        if stop_scraping:
            break  

        key_index = (key_index + 1) % len(api_keys)

    print(f"All queries completed. Results saved to {filename}")

    save_choice = input(f"Do you want to save IP only (Y) or IP:port combinations (N)? ").strip().lower()

    if save_choice == 'y':
        with open(filename, 'r') as f:
            lines = f.readlines()
        with open(filename, 'w') as f:
            for line in lines:
                ip, port = line.strip().split(',')
                f.write(f"{ip}\n")
        print("Saved only IPs to results.txt")
    elif save_choice == 'n':
        print("Saved IPs with ports to results.txt")
    else:
        print("Invalid choice. Saved IPs with ports (default) to results.txt")

if __name__ == "__main__":
    main()
