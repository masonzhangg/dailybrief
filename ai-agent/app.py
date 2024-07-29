import os
from dotenv import load_dotenv
from datetime import datetime

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uvicorn
from ai_agent import sm_summary, sports_summary, tech_summary, normal_news_list, stock_news_item

from supabase import create_client, Client


app = FastAPI()

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class CompanyRequest(BaseModel):
    company_name: str


def insert_summary(supabase_client: Client, table_name: str, summary: str, news_url: str, news_title: str):
    current_date = datetime.now().date()
    data = {
        "date": str(current_date),
        "summary": summary,
        "news_title": news_title,
        "news_url": news_url
    }
    supabase_client.table(table_name).insert(data).execute()


def summarize_and_upload_sports_news(supabase_client: Client):
    news_list = normal_news_list('sports', 10)
    for news in news_list:
        summary = sports_summary(news['content'])
        if 'not relevant' not in summary.lower(): # if the summary is not relevant, skip it
            insert_summary(supabase_client, "sports_summary", summary, news['link'], news['title'])

def summarize_and_upload_tech_news(supabase_client: Client):
    news_list = normal_news_list('technology', 10)
    for news in news_list:
        summary = tech_summary(news['content'])
        if 'not relevant' not in summary.lower():
            insert_summary(supabase_client, "tech_summary", summary, news['link'], news['title'])

def summarize_and_upload_stock_news(supabase_client: Client):
    news_item = stock_news_item('us stock markets', 10)
    if news_item:
        summary = sm_summary(news_item['content'])
        if 'not relevant' not in summary.lower():
            insert_summary(supabase_client, "stock_summary", summary, news_item['link'], news_item['title'])


@app.post("/upload_all/")
async def upload_all(background_tasks: BackgroundTasks):
    background_tasks.add_task(summarize_and_upload_sports_news, supabase)
    background_tasks.add_task(summarize_and_upload_tech_news, supabase)
    background_tasks.add_task(summarize_and_upload_stock_news, supabase)
    return {"message": "Uploading all news"}





# Run the server only if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

    # print("开始测试 summarize_and_upload_stock_news 函数")
    # supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    # try:
    #     summarize_and_upload_stock_news(supabase)
    #     print("函数执行成功")
    # except Exception as e:
    #     print(f"函数执行出错: {e}")
    # print("测试结束")
