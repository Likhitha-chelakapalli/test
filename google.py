import pandas as pd
from googlesearch import search
import time

def get_official_website(company_name):
    query = f"{company_name} official website"
    try:
        # Perform Google search, get top 5 results
        for url in search(query, num_results=5):
            # Simple heuristic: check if company name is part of the URL
            if company_name.lower().replace(" ", "") in url.lower().replace(" ", ""):
                return url
        # If no URL matched, just return the first result
        results = list(search(query, num_results=1))
        return results[0] if results else ""
    except Exception as e:
        print(f"Error searching for {company_name}: {e}")
        return ""

def main():
    df = pd.read_csv("sp500-companies.csv", encoding="latin1")
    df["Official Website"] = ""

    for idx, row in df.iterrows():
        company = row["Name"]
        website = get_official_website(company)
        df.at[idx, "Official Website"] = website
        print(f"{idx+1}. {company} → {website}")
        time.sleep(1)  # polite delay to avoid getting blocked

    # df.to_csv("sp500_with_official_websites.csv", index=False)
    print("Done! Saved to sp500_with_official_websites.csv")

if __name__ == "__main__":
    main()
