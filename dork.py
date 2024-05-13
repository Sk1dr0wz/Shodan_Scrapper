import shodan
import configparser
from colorama import Fore, Style
import argparse

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

        if start >= total_results:
            return True  
    except Exception as e:
        print("Error:", e)

    return False  

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
{"pip install -r requirements.txt".center(80)}
{Fore.WHITE}════════════════════════════════════════════════════════════════════════════════════════""")

    parser = argparse.ArgumentParser(description='Shodan Scrapper Tool')
    parser.add_argument('-q', '--query', help='Shodan dork query', required=True)
    parser.add_argument('-t', '--total_results', type=int, default=1000, help='Total number of results to retrieve (1000 Results equal to 1 Query)')
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

if __name__ == "__main__":
    main()
