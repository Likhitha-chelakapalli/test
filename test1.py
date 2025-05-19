import requests
import pandas as pd


def get_official_website_wikipedia(company_name):
    search_url = "https://en.wikipedia.org/w/api.php"

    # Step 1: Search for the company page title
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

        # Step 2: Get external links from the page
        page_info_params = {
            "action": "query",
            "prop": "extlinks",
            "titles": page_title,
            "format": "json",
            "ellimit": "max"
        }

        page_resp = requests.get(search_url, params=page_info_params, timeout=5)
        page_data = page_resp.json()
        pages = page_data.get("query", {}).get("pages", {})

        for page_id in pages:
            extlinks = pages[page_id].get("extlinks", [])
            for link_obj in extlinks:
                link = list(link_obj.values())[0]

                # Only return URLs that look like real websites
                if link.startswith("http://") or link.startswith("https://"):
                    if company_name.lower().replace(" ", "") in link.lower().replace(" ", ""):
                        return link
            # Fallback: return the first link if no match
            if extlinks:
                return list(extlinks[0].values())[0]
        return ""

    except Exception as e:
        print(f"Error fetching Wikipedia data for {company_name}: {e}")
        return ""


# Step 3: Load Excel file
df = pd.read_excel("sp500-companies.xlsx")
df["Official Website"] = ""

# Step 4: Fetch website for each company
for idx, row in df.iterrows():
    company = row["Name"]
    website = get_official_website_wikipedia(company)
    df.at[idx, "Official Website"] = website
    print(f"{idx + 1}. {company} → {website}")

# Step 5: Save results to new Excel file
df.to_exce("company_website/sp500_with_official_websites.xlsx", index=False)
print("✅ Done! Saved to sp500_with_official_websites.xlsx")
