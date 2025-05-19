import requests
import pandas as pd

def get_official_website_wikipedia(company_name):
    search_url = "https://en.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": company_name,
        "format": "json",
        "srlimit": 1
    }
    try:
        search_resp = requests.get(search_url, params=search_params, timeout=5)
        search_data = search_resp.json()
        search_results = search_data.get("query", {}).get("search", [])
        if not search_results:
            return ""
        page_title = search_results[0]["title"]

        # Get external links from the Wikipedia page
        page_info_params = {
            "action": "query",
            "prop": "extlinks",
            "titles": page_title,
            "format": "json"
        }
        page_resp = requests.get(search_url, params=page_info_params, timeout=5)
        page_data = page_resp.json()
        pages = page_data.get("query", {}).get("pages", {})
        for page_id in pages:
            extlinks = pages[page_id].get("extlinks", [])
            for link_obj in extlinks:
                link = list(link_obj.values())[0]
                if company_name.lower().replace(" ", "") in link.lower().replace(" ", ""):
                    return link
            if extlinks:
                return extlinks[0].get("*", "")
        return ""
    except Exception as e:
        print(f"Error fetching Wikipedia data for {company_name}: {e}")
        return ""

# Load Excel file
input_file = "sp500-companies.xlsx"
df = pd.read_excel(input_file)

# Add a new column for official websites
df["Official Website"] = ""

# Loop through companies and fetch official websites
for idx, row in df.iterrows():
    company = row["Name"]
    website = get_official_website_wikipedia(company)
    df.at[idx, "Official Website"] = website
    print(f"{idx+1}. {company} → {website}")

# Save to new Excel file
output_file = "/company_website/sp500_with_websites_wikipedia.xlsx"
df.to_excel(output_file, index=False)
print(f"Done! Saved to {output_file}")
