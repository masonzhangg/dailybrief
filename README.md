# DailyBriefs


## [News Summarization Backend](https://github.com/andrewangbl/backend-hackathon)

This project is a backend service that automatically fetches, summarizes, and stores news articles from various categories using AI-powered summarization.

### How It Works

The backend follows a pipeline to process news articles:

1. **Fetching News URLs**: The system searches for news articles using Google News.
2. **Web Scraping**: It then scrapes the content from the news websites.
3. **AI Summarization**: The scraped content is summarized using AI models.
4. **Database Storage**: Finally, the summaries are stored in a Supabase database.

#### Detailed Pipeline

##### 1. Fetching News URLs

- The `getNewsData` function in `ai_agent.py` searches Google News for articles based on a query and number of results.
- For stock news, `get_stock_news_data` is used to specifically fetch Yahoo Finance articles.

##### 2. Web Scraping

- The `get_news_data_from_url` function in `ai_agent.py` scrapes the content from each news URL.
- It uses BeautifulSoup to parse the HTML and extract relevant information like title, text, date, and source.

##### 3. AI Summarization

- Three summarization functions are used for different news categories:
  - `sm_summary` for stock market news
  - `sports_summary` for sports news
  - `tech_summary` for technology news
- These functions use OpenAI's GPT model via the LangChain library to generate summaries.
- Custom prompts are used to guide the AI in creating relevant summaries for each category.

##### 4. Database Storage

- The `insert_summary` function in `app.py` handles storing summaries in Supabase.
- It creates a data object with the current date, summary, news title, and URL.
- The data is then inserted into the appropriate table in Supabase.

#### API Endpoint

- The `/upload_all/` endpoint triggers the summarization and upload process for all news categories.
- It uses FastAPI's `BackgroundTasks` to run the processes asynchronously.

### GPT-3.5-turbo Model Usage
This project utilizes OpenAI's GPT-3.5-turbo model for summarizing news articles. We employ the map-reduce method to efficiently process longer texts while staying within the model's token limit.

#### Map-Reduce Method

The map-reduce approach is implemented using LangChain's `load_summarize_chain` function. This method involves:

1. **Splitting**: The input text is split into smaller chunks.

2. **Mapping**: Each chunk is summarized independently.

3. **Reducing**: The individual summaries are combined into a final summary.

#### Prompt Engineering

We use carefully crafted prompts for each news category (stock market, sports, and technology). These prompts are designed to:


1. **Guide the model**: Instruct the model to act as a specific type of analyst (e.g., "As a stock market analyst...").

2. **Ensure accuracy**: Include instructions like "YOU DO NOT MAKE UP CONTENTS!" to prevent fabrication.

3. **Retain important information**: Request that "all important numbers, statistics, and quotes are retained."

4. **Filter irrelevant content**: Use the instruction "If the content is not related to [category], please respond with *NOT RELEVANT*."

5. **Focus on key points**: Provide a list of specific items to include in the summary if mentioned in the original text.


Example of a map prompt (for stock market news):
```
    map_prompt = """
    As a stock market analyst, please summarize the following news content and extract key market insights and data:

    "{text}"

    YOU DO NOT MAKE UP CONTENTS!

    Please include the following in your summary ONLY if mentioned:
    1. Changes in major market indices (if mentioned)
    2. Performance and reasons for important stocks
    3. Key factors affecting the market (e.g., economic data, company earnings, policy changes, etc.)
    4. Important statistics and percentage changes
    5. Important quotes from analysts or experts
    6. Predictions or opinions on future market trends

    Please ensure all important numbers, statistics, and quotes are retained.
    If the content is not related to the stock market, please respond with *NOT RELEVANT*.

    Summary:
    """
```

### Setup and Running

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `OPENAI_API_KEY`

3. Run the FastAPI server:
   ```
   python app.py
   ```
