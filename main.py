from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import Dict, List, TypedDict, Any
from typing import Annotated
from langchain_core.output_parsers import StrOutputParser
import operator

# Disable telemetry
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_ENDPOINT"] = ""

# Initialize Ollama LLM
try:
    llm = OllamaLLM(
        model="qwen2.5:latest",
        temperature=0.3,
        num_gpu=1
    )
except Exception as e:
    st.error(f"Failed to initialize LLM: {str(e)}")
    st.error("Make sure Ollama is running and the model is downloaded (ollama pull qwen2.5)")
    st.stop()

# Streamlit UI setup
st.set_page_config(page_title="Divar Advertisement Scraper", page_icon="🔍")
st.title("Divar Advertisement Scraper")
st.write("Enter your query and city to find relevant advertisements from Divar.ir")

# Define city mappings (Persian to English transliteration)
persian_to_english = {
    "تبریز": "tabriz",
    "ارومیه": "urmia",
    "اردبیل": "ardabil",
    "اصفهان": "isfahan",
    "کرج": "karaj",
    "ایلام": "ilam",
    "بوشهر": "bushehr",
    "تهران": "tehran",
    "شهرکرد": "shahrekord",
    "بیرجند": "birjand",
    "مشهد": "mashhad",
    "بجنورد": "bojnurd",
    "خوزستان": "ahvaz",
    "زنجان": "zanjan",
    "سمنان": "semnan",
    "زاهدان": "zahedan",
    "شیراز": "shiraz",
    "قزوین": "qazvin",
    "قم": "qom",
    "سنندج": "sanandaj",
    "کرمان": "kerman",
    "کرمانشاه": "kermanshah",
    "یاسوج": "yasuj",
    "گرگان": "gorgan",
    "رشت": "rasht",
    "خرم آباد": "khorramabad",
    "ساری": "sari",
    "اراک": "arak",
    "بندر عباس": "bandar-abas",
    "همدان": "hamedan",
    "یزد": "yazd"
}

# User inputs
user_query = st.text_input("What are you looking for?", placeholder="e.g. apartment for rent")

# Create sorted list of Persian city names for the select box
persian_cities = sorted(persian_to_english)
city_name = st.selectbox("Select a city", persian_cities, index=0)

def normalize_city(city_input: str) -> str:
    """Normalize city name for URL"""
    # Check if input is Persian
    for persian, english in persian_to_english.items():
        if city_input == persian:
            return english
    
    # Assume it's English, normalize
    normalized = city_input.lower().replace(" ", "-")
    if normalized in persian_to_english.values():
        return normalized
    
    raise ValueError(f"Invalid city name: {city_input}")

def generate_search_query(user_query: str) -> str:
    """Generate optimized search query from user input"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a search query optimizer. Extract the most important keyword from the user's query."),
        ("user", f"Extract the most relevant keywords for searching from: {user_query}. it must be atmost two words and not have words like Keyword. it is better to be persian meaningful words.")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"user_query": user_query})

def scrape_divar_ads(city: str, search_query: str) -> str:
    """Scrapes advertisements from Divar.ir with infinite scrolling"""
    try:
        # Normalize city name
        city_normalized = normalize_city(city)
        url = f"https://divar.ir/s/{city_normalized}?q={search_query}"
        
        # Set up Selenium with headless Chrome
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        driver = webdriver.Chrome(options=options)
        
        try:
            # Load page
            driver.get(url)
            time.sleep(3)  # Initial load wait
            
            # Infinite scroll implementation
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scroll_attempts = 60 # Safety limit
            
            while scroll_attempts < max_scroll_attempts:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait for content to load
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break  # No more content to load
                
                last_height = new_height
                scroll_attempts += 1
            
            # Parse page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Extract ad elements
            output = ""
            post_cards = soup.find_all('div', class_=lambda x: x and "post-card" in x)
            
            for card in post_cards:
                
                    title = card.find('h2', class_=lambda x: x and "title" in x.lower())
                    description = card.find('div', class_=lambda x: x and "description" in x.lower())
                    price = card.find('div', class_=lambda x: x and "price" in x.lower())
                    
                    title_text = title.get_text(strip=True) if title else "No title"
                    desc_text = description.get_text(strip=True) if description else "No description"
                    price_text = price.get_text(strip=True) if price else "Price not specified"
                    
                    output += f"- **{title_text}**\n  - Price: {price_text}\n  - Description: {desc_text}\n\n"
            
            return output if output else "No advertisements found matching your criteria."
            
        finally:
            driver.quit()
            
    except Exception as e:
        return f"Error scraping ads: {str(e)}"


# Define AgentState with custom state structure
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    city: str
    query: str
    optimized_query: str
    relevant_ads: str

# Define nodes for the graph
def initialize_state(state: AgentState) -> Dict[str, Any]:
    """Initialize the agent state"""
    return {
        "messages": [HumanMessage(content=f"I'm looking for {state['query']} in {state['city']}")],
        "city": state["city"],
        "query": state["query"],
        "optimized_query": "",
        "relevant_ads": ""
    }

def optimize_query(state: AgentState) -> Dict[str, Any]:
    """Optimize the user query into a search keyword"""
    optimized_query = generate_search_query(state["query"])
    return {
        "messages": [AIMessage(content=f"Optimized search query: {optimized_query}")],
        "city": state["city"],
        "query": state["query"],
        "optimized_query": optimized_query,
        "relevant_ads": ""
    }

def run_agent(state: AgentState) -> Dict[str, Any]:
    """Run the agent"""
    output = scrape_divar_ads(state["city"], state["optimized_query"])
    template = """You are a helpful traveller assistant that finds relevant advertisements from scraped data from Divar.ir.
    according to this scraped data: {output}, make a bulleted list that contains the title, description and price of relevant advertisements. Do not explain more details.
    just showing the distinct advertisements.
    relevant_advertisements:"""
    prompt = ChatPromptTemplate.from_template(template=template)
    chain = prompt | llm | StrOutputParser()
    relevant_ads = chain.invoke({"output": output})
    
    return {
        "messages": [AIMessage(content=relevant_ads)],
        "city": state["city"],
        "query": state["query"],
        "optimized_query": state["optimized_query"],
        "relevant_ads": relevant_ads
    }
    

# Build the workflow graph
workflow = StateGraph(AgentState)

# Define nodes
workflow.add_node("initialize", initialize_state)
workflow.add_node("optimize_query", optimize_query)
workflow.add_node("search", run_agent)

# Define edges
workflow.add_edge("initialize", "optimize_query")
workflow.add_edge("optimize_query", "search")
workflow.add_edge("search", END)

# Set entry point
workflow.set_entry_point("initialize")

# Compile the graph
app = workflow.compile()

if st.button("Search Divar"):
    if not user_query or not city_name:
        st.warning("Please enter both a query and city name")
    else:
        with st.spinner("Processing your request..."):
            try:
                # Initialize state
                initial_state: AgentState = {
                    "messages": [],
                    "city": city_name,
                    "query": user_query,
                    "optimized_query": "",
                    "relevant_ads": ""
                }
                
                # Execute the workflow
                final_state = app.invoke(initial_state)
                
                # Display results
                if final_state and "messages" in final_state:
                    st.subheader("Search Results")
                    for message in final_state["messages"]:
                        if isinstance(message, AIMessage):
                            st.markdown(message.content)
                    st.success("Search completed!")
                else:
                    st.error("No results found or an error occurred during processing.")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("""
                Troubleshooting steps:
                1. Ensure Ollama is running (ollama serve)
                2. Check Chrome and chromedriver versions match
                3. Try a simpler query or different city
                """)