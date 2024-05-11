import shodan
import configparser
from colorama import Fore, Style

def perform_search(query, filename, start, api_key, total_results):
    api = shodan.Shodan(api_key)

    try:
        results = api.search(query, page=start // 1000 + 1)
        with open(filename, "a") as f:
            for result in results['matches']:
                ip = result['ip_str']
                port = result['port']
                hostname = result['hostnames'][0] if result['hostnames'] else ''
                os_info = result['os']
                f.write(f"{ip},{port},{hostname},{os_info}\n")

        print(f"Query {start // 1000 + 1} completed.")

        # Check if we have retrieved all desired results
        if start >= total_results:
            return True  # Signal to stop further queries
    except Exception as e:
        print("Error:", e)

    return False  # Continue querying

def main():
    print(f"""{Style.BRIGHT + Fore.RED}

███████╗██╗  ██╗ ██╗██████╗ ██████╗  ██████╗ ██╗    ██╗███████╗
██╔════╝██║ ██╔╝███║██╔══██╗██╔══██╗██╔═████╗██║    ██║╚══███╔╝
███████╗█████╔╝ ╚██║██║  ██║██████╔╝██║██╔██║██║ █╗ ██║  ███╔╝ 
╚════██║██╔═██╗  ██║██║  ██║██╔══██╗████╔╝██║██║███╗██║ ███╔╝  
███████║██║  ██╗ ██║██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝███████╗
╚══════╝╚═╝  ╚═╝ ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝

{Fore.WHITE}════════════════════════════════════════════════════════════════════════════════════════
{Style.BRIGHT + Fore.YELLOW}{"Coded by sk1dr0wz".center(80)}
{"Shodan Scrapper Tool".center(80)}
{"Copyright By: Hamba Abdi".center(80)}
{Fore.WHITE}════════════════════════════════════════════════════════════════════════════════════════""")

    # Read API key from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    shodan_api_key = config['API_KEYS']['SHODAN_API_KEY']

    # Minimum Total Results Is 1000 = 1 Query
    query = input("Enter your Shodan dork query: ")
    total_results = int(input("Enter the total number of results you want to retrieve: "))
    chunk_size = 1000
    num_queries = total_results // chunk_size

    filename = "results.txt"

    api_keys = [shodan_api_key]

    key_index = 0

    for i in range(num_queries):
        start_index = i * chunk_size
        stop_scraping = perform_search(query, filename, start_index, api_keys[key_index], total_results)

        if stop_scraping:
            break  # Stop making further queries

        key_index = (key_index + 1) % len(api_keys)

    print(f"All queries completed. Results saved to {filename}")

if __name__ == "__main__":
    main()