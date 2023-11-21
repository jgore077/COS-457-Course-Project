import requests

# Match Search
match_search_url = "http://localhost:3000/search_matches"
match_params = {
    'date': '2021-11-25',
    'location': 'USM'
}

match_response = requests.get(match_search_url, params=match_params)
print("Match Search - Status Code:", match_response.status_code)
print("Match Search - Response Text:", match_response.text)
print(match_response.json())

# News Search
news_search_url = "http://localhost:3000/search_news"
news_params = {
    'date_published': '2019-07-04',
    'content': 'Match Cancellation'
}

news_response = requests.get(news_search_url, params=news_params)
print("News Search - Status Code:", news_response.status_code)
print("News Search - Response Text:", news_response.text)
print(news_response.json())
