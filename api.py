from serpapi import GoogleSearch
# search_for = input("Search For:")
def process_api(label):
  params = {
    "engine": "google_shopping",
    "q": label,
    "location": "Hyderabad, Telangana, India",
    "hl": "en",
    "gl": "us",
    "api_key": "a164100af83232644c07415f63b89174cab87a3f64abe0c6ee03b86711d06a6c"
  }
  search = GoogleSearch(params)
  results = search.get_dict()
  shopping_results = results["shopping_results"]
  # print(shopping_results)
  return shopping_results