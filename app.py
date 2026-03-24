import streamlit as st
import os
import datetime
from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
import pandas as pd
import sqlite3

# Set your API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

@st.cache_resource
def get_agent():
    # Initialize the database if it doesn't exist
    if not os.path.exists('climate.db'):
        conn = sqlite3.connect('climate.db')
        conn.close()

    # Initialize the model
    model = init_chat_model("gpt-4o-mini",temperature=0.1)

    # Configure the database
    db = SQLDatabase.from_uri("sqlite:///climate.db")

    # Add tools for database interaction
    toolkit = SQLDatabaseToolkit(db=db, llm=model)
    tools = toolkit.get_tools()

    system_prompt = """
    You are an agent designed to interact with a SQL database about
    global climate and energy data spanning 20 countries from 2020 to 2024.

    Given an input question, create a syntactically correct {dialect} query to run,
    then look at the results of the query and return the answer. Unless the user
    specifies a specific number of examples they wish to obtain, always limit your
    query to at most {top_k} results.

    You can order the results by a relevant column to return the most interesting
    examples in the database. Never query for all the columns from a specific table,
    only ask for the relevant columns given the question.

    You MUST double check your query before executing it. If you get an error while
    executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
    database.

    To start you should ALWAYS look at the tables in the database to see what you
    can query. Do NOT skip this step.

    Then you should query the schema of the most relevant tables.

    Additional instructions specific to this database:
    - The database contains daily climate and energy records for 20 countries:
      Germany, France, Netherlands, Italy, Spain, Sweden, Norway, Poland, Turkey,
      United Kingdom, United States, Canada, Brazil, India, China, Japan, Australia,
      South Africa, Mexico, Indonesia.
    - CRITICAL: When users refer to USA or US, query the database using 'United States'.
    - CRITICAL: When users refer to any country, look up the exact country name from the list above
      and use that exact name (with correct capitalization) in your SQL WHERE clause.
    - Key columns are: date, country, avg_temperature, humidity, co2_emission,
      energy_consumption, renewable_share, urban_population,
      industrial_activity_index, energy_price.
    - When comparing countries always use AVG() to get meaningful comparisons
      since data is daily.
    - When asked about trends always GROUP BY year or month using
      strftime('%Y', date) or strftime('%Y-%m', date).
    - When asked about renewable energy use the renewable_share column.
    - When asked about pollution or emissions use the co2_emission column.
    - Always present numbers rounded to 2 decimal places using ROUND().
    - When ranking countries always use ORDER BY and AVG() together.
    """.format(
        dialect=db.dialect,
        top_k=5,
    )

    agent = create_agent(
        model,
        tools,
        system_prompt=system_prompt,
    )
    return agent

agent = get_agent()

# Initialize session state for messages and selected country
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_country" not in st.session_state:
    st.session_state.selected_country = "No selection"
if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0

# Weather mode based on prompt count
weather_mode = "sun" if st.session_state.prompt_count % 2 == 0 else "rain"

# Title and description plus dynamic layout
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
  background-image: linear-gradient(rgba(8, 84, 90, 0.65), rgba(20, 113, 135, 0.35)), url('https://images.unsplash.com/photo-1517816743773-6e0fd518b4a6?crop=entropy&cs=tinysrgb&fm=jpg&ixlib=rb-4.0.3&auto=format&fit=crop&w=1850&q=80');
  background-attachment: fixed;
  background-position: center;
  background-size: cover;
  color: #ffffff;
  position: relative;
}

[data-testid="stAppViewContainer"]::before {
  content: "";
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(120deg, rgba(255, 214, 102, 0.22), rgba(56, 153, 212, 0.28));
  pointer-events: none;
  z-index: 0;
}

.weather-overlay {
  position: fixed;
  right: 20px;
  top: 20px;
  width: 140px;
  height: 140px;
  z-index: 10;
  pointer-events: none;
  opacity: 0.9;
}

.weather-element {
  position: absolute;
  inset: 0;
  opacity: 0;
}

@keyframes weatherCycle {
  0%, 32.999% { opacity: 1; }
  33%, 100% { opacity: 0; }
}

.sun-element {
  animation: weatherCycle 30s linear infinite;
}

.rain-element {
  animation: weatherCycle 30s linear infinite;
  animation-delay: 10s;
}

.snow-element {
  animation: weatherCycle 30s linear infinite;
  animation-delay: 20s;
}


.sun-ball {
  position: absolute;
  right: 0;
  top: 0;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, #fff8b4, #ffd55d 60%, #ffbc33);
  box-shadow:
    0 0 30px rgba(255, 214, 102, 0.9),
    0 0 45px rgba(255, 187, 51, 0.65),
    0 0 20px rgba(255, 140, 0, 0.8) inset,
    0 0 60px rgba(255, 200, 50, 0.4),
    0 0 80px rgba(255, 160, 0, 0.3);
  animation: sun-pulse 10s ease-in-out infinite;
  position: relative;
}

.sun-ball::before {
  content: '';
  position: absolute;
  top: -15px;
  left: -15px;
  right: -15px;
  bottom: -15px;
  border-radius: 50%;
  background: radial-gradient(circle, transparent 40%, rgba(255, 200, 50, 0.3) 50%, rgba(255, 140, 0, 0.2) 70%, transparent 80%);
  animation: solar-flare 3s ease-in-out infinite alternate;
}

.sun-ball::after {
  content: '';
  position: absolute;
  top: -25px;
  left: -25px;
  right: -25px;
  bottom: -25px;
  border-radius: 50%;
  background: conic-gradient(from 0deg, rgba(255, 200, 50, 0.1), transparent 60deg, rgba(255, 140, 0, 0.15) 120deg, transparent 180deg, rgba(255, 200, 50, 0.1) 240deg, transparent 300deg);
  animation: solar-flare-rotate 8s linear infinite;
}

@keyframes solar-flare {
  0% { transform: scale(1); opacity: 0.3; }
  100% { transform: scale(1.2); opacity: 0.6; }
}

@keyframes solar-flare-rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes sun-pulse {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(25px) scale(1.1); }
}

.rain-container {
  position: absolute;
  width: 140px;
  height: 140px;
}

.rain-drop {
  position: absolute;
  width: 24px;
  height: 24px;
  color: rgba(176, 214, 255, 0.95);
  font-size: 20px;
  line-height: 24px;
  text-align: center;
  animation: fall 1.8s linear infinite;
}

.rain-drop::after {
  content: "💧";
  display: block;
}

@keyframes fall {
  0% { transform: translateY(-20px) scaleY(1); opacity: 0; }
  20% { opacity: 1; }
  100% { transform: translateY(120px) scaleY(1.6); opacity: 0; }
}

.snow-container {
  position: absolute;
  width: 140px;
  height: 140px;
}

.snowflake {
  position: absolute;
  width: 22px;
  height: 22px;
  color: #f8faff;
  font-size: 20px;
  line-height: 22px;
  text-align: center;
  animation: snow-fall 4.5s linear infinite;
}

.snowflake::after {
  content: "❄";
  display: block;
  transform: rotate(0deg);
}

@keyframes snow-fall {
  0% { transform: translateY(-20px) translateX(0) rotate(0deg); opacity: 0; }
  20% { opacity: 1; }
  100% { transform: translateY(130px) translateX(15px) rotate(45deg); opacity: 0; }
}

.wind-container {
  position: absolute;
  width: 140px;
  height: 140px;
}

.wind-cloud {
  position: absolute;
  width: 42px;
  height: 24px;
  background: rgba(245, 248, 255, 0.86);
  border-radius: 50%;
  box-shadow: 12px 0 0 rgba(245, 248, 255, 0.86), 24px 0 0 rgba(245, 248, 255, 0.86);
  opacity: 0.85;
  animation: cloud-move 8s linear infinite;
}

@keyframes cloud-move {
  0% { transform: translateX(-60px); opacity: 0.7; }
  45% { opacity: 1; }
  100% { transform: translateX(160px); opacity: 0.7; }
}

@keyframes wind-move {
  0% { transform: translateX(-40px); }
  100% { transform: translateX(180px); }
}

.stSidebar {
  background-color: rgba(1, 56, 83, 0.8);
  border-right: 1px solid rgba(255, 255, 255, 0.18);
}

.stMarkdown p, .stMarkdown li {
  color: #f7faff;
}

h1, h2, h3, h4, h5, h6 {
  color: #edeff3;
}

.stChatMessage {
  background: rgba(22, 49, 71, 0.66) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

</style>
<div id="weather-overlay" class="weather-overlay weather-sun">
  <div class="weather-element weather-sun">
    <div class="sun-ball"></div>
  </div>
  <div class="weather-element weather-rain rain-container">
    <div class="rain-drop" style="left: 12px; animation-delay: 0.1s;"></div>
    <div class="rain-drop" style="left: 35px; animation-delay: 0.3s;"></div>
    <div class="rain-drop" style="left: 58px; animation-delay: 0.6s;"></div>
    <div class="rain-drop" style="left: 80px; animation-delay: 0.45s;"></div>
    <div class="rain-drop" style="left: 102px; animation-delay: 0.8s;"></div>
  </div>
  <div class="weather-element weather-snow snow-container">
    <div class="snowflake" style="left: 10px; animation-delay: 0.2s;"></div>
    <div class="snowflake" style="left: 45px; animation-delay: 0.8s;"></div>
    <div class="snowflake" style="left: 80px; animation-delay: 0.45s;"></div>
    <div class="snowflake" style="left: 110px; animation-delay: 1.1s;"></div>
  </div>
</div>
</style>
<div id="weather-overlay" class="weather-overlay">
  <div class="weather-element weather-sun sun-element">
    <div class="sun-ball"></div>
  </div>
  <div class="weather-element weather-rain rain-element rain-container">
    <div class="rain-drop" style="left: 12px; animation-delay: 0.1s;"></div>
    <div class="rain-drop" style="left: 35px; animation-delay: 0.3s;"></div>
    <div class="rain-drop" style="left: 58px; animation-delay: 0.6s;"></div>
    <div class="rain-drop" style="left: 80px; animation-delay: 0.45s;"></div>
    <div class="rain-drop" style="left: 102px; animation-delay: 0.8s;"></div>
  </div>
  <div class="weather-element weather-snow snow-element snow-container">
    <div class="snowflake" style="left: 10px; animation-delay: 0.2s;"></div>
    <div class="snowflake" style="left: 45px; animation-delay: 0.8s;"></div>
    <div class="snowflake" style="left: 80px; animation-delay: 0.45s;"></div>
    <div class="snowflake" style="left: 110px; animation-delay: 1.1s;"></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.title("🌍 SQL Climate Agent")
st.markdown("""
Ask questions about global climate and energy data spanning 20 countries from 2020 to 2024.
The agent can query the database and provide insights on temperature, emissions, energy consumption, and more.
""")

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    
    # Date range selector
    st.subheader("📅 Select date range (Optional)")
    default_start = datetime.date(2020, 1, 1)
    default_end = datetime.date(2024, 12, 31)
    date_range = st.date_input(
        "Choose date range:",
        value=(default_start, default_end),
        min_value=default_start,
        max_value=default_end,
        key="date_range_selector",
    )

    # Country selector dropdown
    st.subheader("🌍 Select Country (Optional)")
    countries = [
        "No selection",
        "Germany",
        "France",
        "Netherlands",
        "Italy",
        "Spain",
        "Sweden",
        "Norway",
        "Poland",
        "Turkey",
        "United Kingdom",
        "United States",
        "Canada",
        "Brazil",
        "India",
        "China",
        "Japan",
        "Australia",
        "South Africa",
        "Mexico",
        "Indonesia",
    ]
    st.session_state.selected_country = st.multiselect(
        "Filter by country:",
        countries,
        # index=0,
        key="country_selector"
    )
    
    st.markdown("""
    **Database:** SQLite with daily climate records
            
    **Key Metrics:**
    - Average Temperature
    - CO2 Emissions
    - Energy Consumption
    - Renewable Share
    - And more...
    """)
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about the climate data..."):
    # Toggle prompt count so first prompt -> rain, second -> sun, etc.
    st.session_state.prompt_count += 1

    # Construct targeted context
    selected = []
    if st.session_state.selected_country != "No selection":
        selected.append(f"country = {st.session_state.selected_country}")

    date_range = st.session_state.get("date_range_selector", None)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        if start_date != datetime.date(2020, 1, 1) or end_date != datetime.date(2024, 12, 31):
            selected.append(f"date between {start_date} and {end_date}")

    enhanced_prompt = prompt
    if selected:
        enhanced_prompt += "\n\n(Please focus on data for " + ", ".join(selected) + ")"

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        steps = []
        
        response_placeholder.info("🤔 Thinking...")
        
        try:
            for step in agent.stream(
                {"messages": [{"role": "user", "content": enhanced_prompt}]},
                stream_mode="values",
            ):
                message = step["messages"][-1]
                if hasattr(message, 'content') and message.content:
                    steps.append(message.content)
        except Exception as e:
            steps.append(f"An error occurred: {str(e)}")
        
        # Clear the thinking message
        response_placeholder.empty()
        
        # Show all steps in expandable section
        if steps:
            with st.expander("📋 View Agent Steps"):
                for i, step in enumerate(steps, 1):
                    st.markdown(f"**Step {i}:**")
                    st.markdown(step)
        
        # Display only final answer
        final_answer = steps[-1] if steps else "No response"
        st.markdown(final_answer)
    
    # Add assistant message to session state
    st.session_state.messages.append({"role": "assistant", "content": final_answer})