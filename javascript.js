function getCompanyWikipediaWebsite(companyName) {
    if (!companyName) return "No Company Name";
    
    const searchQuery = encodeURIComponent(companyName);
    const searchUrl = `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${searchQuery}%20company&format=json&origin=*`;
  
    try {
      const searchResponse = UrlFetchApp.fetch(searchUrl);
      const searchData = JSON.parse(searchResponse.getContentText());
  
      if (!searchData.query || searchData.query.search.length === 0)
        return "Wikipedia page not found";
  
      const pageTitle = searchData.query.search[0].title;
      const pageDetailsUrl = `https://en.wikipedia.org/w/api.php?action=query&prop=extlinks&titles=${encodeURIComponent(pageTitle)}&format=json&origin=*`;
  
      const pageResponse = UrlFetchApp.fetch(pageDetailsUrl);
      const pageData = JSON.parse(pageResponse.getContentText());
  
      const pages = pageData.query.pages;
      const pageId = Object.keys(pages)[0];
  
      if (!pages[pageId].extlinks) return "Website not listed";
  
      const links = pages[pageId].extlinks;
      
      // Try to find the official website link (first non-wiki link usually)
      for (let i = 0; i < links.length; i++) {
        const url = links[i]["*"];
        if (url.includes(".com") && !url.includes("wikipedia")) {
          return url;
        }
      }
  
      return "Website not listed";
  
    } catch (e) {
      return "Error: " + e.message;
    }
  }
  