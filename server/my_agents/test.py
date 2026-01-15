import argparse
import pandas as pd
from scraper import scrape_nearby

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Maps Nearby Scraper")
    parser.add_argument("--address", type=str, required=True, help="Target Address (Start Point)")
    parser.add_argument("--query", type=str, required=True, help="Category to search (e.g. 'restaurants')")
    args = parser.parse_args()
    
import asyncio

async def main(address, query):
    data = await scrape_nearby(address, query)
    
    # Save to CSV
    if data:
        df = pd.DataFrame(data)
        df.to_csv("nearby_results.csv", index=False)
        print("Saved to nearby_results.csv")
    else:
        print("No data found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Maps Nearby Scraper")
    parser.add_argument("--address", type=str, required=True, help="Target Address (Start Point)")
    parser.add_argument("--query", type=str, required=True, help="Category to search (e.g. 'restaurants')")
    args = parser.parse_args()
    
    asyncio.run(main(args.address, args.query))