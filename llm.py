import os
import streamlit as st
from openai import OpenAI
import textwrap

os.environ["OPENAI_API_KEY"] = st.secrets['OPENAI_API_KEY']

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

def generate_query(query):
    prompt = f'''Given a user's prompt for news articles about a specific area of interest like a company, a topic, or a person, generate a query with the right parameters from the user's prompt incorporated into it. 
    If the user's query seems to be focused on a company or an individual, insert the name of that company or individual into the surface_forms.text attribute of the entity attribute to generate the query. If you know the Wikidata ID for that company or individual, add it with an OR operator to the entity query.
    If the user's query seems to be focused on a topic or concept, describe that topic or concept in up to 5 keywords or key phrases (each keyword or keyphrase must be wrapped in double quotes).
    If the user's query seems to be focused on an event like a car crash, a new product release, a terrorist attack, or an earthquake, write up to 5 keywords or short phrases that describe that event happening and put it in the title part of the text attribute to generate a query. 
    If an industry or business sector is mentioned in the query, include it in the query as a couple of keywords or keyphrases using an AND operator.
    On the second line of the query, insert the time range the user has specified in their prompt, in the format {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}} and replace the start and end values with values from the user's prompt.
    When the query is about news published in a certain country, use the 'source.locations.country' attribute and insert the 2 letter country ID for that country. But when the news is requested about a country, add the country as an entity. 
    
    Examples:

    prompt: Show me all the articles about Aylien, an AI company based in Ireland, that were written in the last 24 hours
    query:
    entities:({{{{surface_forms.text:"aylien" AND overall_prominence:>=0.65}}}})
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: Show me all the articles about Apple
    query:
    entities:({{{{(surface_forms.text:"apple" OR id:Q312) AND overall_prominence:>=0.65}}}})
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: What's the latest news about ESG?
    query:
    title:("ESG" OR ("Environmental" AND "Social" AND "Governance"))
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: What's the latest news about ESG in banking?
    query:
    title:(("ESG" OR ("Environmental" AND "Social" AND "Governance")) AND ("banking" OR "banks"))
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: The latest news about tech acquisitions
    query:
    title:(("acquisitions" OR "acquired" OR "merger" OR "merges") AND ("technology" OR "technology startup" OR "tech company"))
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: What are the latest articles about politics?
    query:
    title:("Politics" OR "Politicians" OR "World politics")
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}
    
    prompt: What are the latest articles about Elon Musk that don't mention SpaceX?
    query:
    title:("Elon Musk" NOT "SpaceX")
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: Show me all the articles about Steve Jobs
    query:
    entities:({{{{(surface_forms.text:"Steve Jobs" OR id:Q19837) AND overall_prominence:>=0.65}}}})
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: What's in the news about Wells Fargo?
    query: 
    entities:({{{{(surface_forms.text:"Wells Fargo", id:Q744149) AND overall_prominence:>=0.65}}}})
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: What's in the news about Elon Musk's companies?
    query: 
    entities:({{{{(surface_forms.text:"Tesla" OR id:Q478214) AND overall_prominence:>=0.65}}}} OR {{{{(surface_forms.text:"SpaceX" OR id:Q193701) AND overall_prominence:>=0.65}}}} OR {{{{(surface_forms.text:"OpenAI" OR id:Q21708200) AND overall_prominence:>=0.65}}}})
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: What news do you have about car crashes?
    query:
    title:("car has crashed" OR "car crashed" OR "car crash" OR "road accident")
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: Show me all the articles about Iran's president
    query:
    entities:({{{{surface_forms.text:"Hassan Rouhani" AND overall_prominence:>=0.65}}}})
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: What happened in Finland last week?
    query:
    entities:({{{{surface_forms.text:"finland" AND element:title}}}})
    {{"published_at.start": "NOW-14DAYS", "published_at.end": '7DAYS'}}

    prompt: What cyber security events happened in Australia within the pharmaceutical industry last month?
    query:
    title:("pharmaceuticals" OR "pharma") AND ("hacking" OR "hacked") AND entities:({{{{(id:Q408 OR surface_forms.text:"australia") AND overall_prominence:>=0.65 AND element:title}}}})
    {{"published_at.start": "NOW-2MONTHS", "published_at.end": '1MONTH'}}

    prompt: What positive news has been published about Joe Biden on gun control?
    query:
    title:("gun control" OR "guns" OR "shooting") AND entities:({{{{(id:Q6279 OR surface_forms.text:"joe biden") AND overall_prominence:>=0.65}}}}) AND sentiment.title.polarity:(positive)
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: What negative news has been published about Donald Trump and Twitter?
    query:
    entities:({{{{(id:Q22686 OR surface_forms.text:"donald trump") AND overall_prominence:>=0.65}}}}) AND entities:({{{{(id:Q918 OR surface_forms.text:"twitter") AND overall_prominence:>=0.65}}}}) AND sentiment.title.polarity:(negative)
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: What's in the news today about Elon Musk and Michael Burry?
    query:
    entities:({{{{(surface_forms.text:"Elon Musk" OR id:Q317521) AND overall_prominence:>=0.65}}}} AND {{{{(surface_forms.text:"Michael Burry" OR id:Q6828961) AND overall_prominence:>=0.65}}}})
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW"}}

    prompt: What's being said positively about Jeff Bezos in India and United Kingdom?
    query:
    entities:({{{{(surface_forms.text:"Jeff Bezos" OR id:Q312556) AND overall_prominence:>=0.65}}}} AND sentiment.title.polarity:(positive)
    {{"published_at.start": "NOW-7DAYS", "published_at.end": "NOW", "source.locations.country": [["IN", "UK"]]}}

    prompt: What happened in biotech 3 months ago in Saudi Arabia?
    query:
    title:("biotech" OR "biotechnology" OR "biotech industry")
    {{"published_at.start": "NOW-4MONTHS", "published_at.end": "NOW-3MONTHS", "source.locations.country": [["SA"]]}}

    prompt: {query}
    query:'''
    
    prompt = textwrap.dedent(prompt)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4-turbo",
    )
    return chat_completion.choices[0].message.content

def summarise_news(headlines, num_sentences):
    prompt = f'''Given the following list of news headlines, summarise them into a single paragraph with {num_sentences} sentences. 
    Headlines: 
    {headlines} 
    Summary:'''
    
    prompt = textwrap.dedent(prompt)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o",
    )
    return chat_completion.choices[0].message.content