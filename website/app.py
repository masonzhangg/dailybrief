from flask import Flask, render_template, jsonify
from supabase import create_client, Client
from datetime import date

app = Flask(__name__)

# Supabase connection setup
supabase_url = "xxx.co"
supabase_key = "xxx"
supabase: Client = create_client(supabase_url, supabase_key)

def get_articles_from_supabase(table):
    today = date.today().isoformat()  # Get today's date in ISO format
    response = supabase.table(table).select('news_title, summary, news_url').eq('date', today).limit(3).execute()
    if response.data:
        articles = [{'title': row['news_title'], 'summary': row['summary'], 'url': row['news_url']} for row in response.data]
        return articles
    else:
        raise Exception(f"Error fetching articles: {response}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_articles/<category>')
def get_articles(category):
    try:
        table_mapping = {
            'sports': 'sports_summary',
            'technology': 'tech_summary',
            'stock_market': 'stock_summary'
        }
        table = table_mapping.get(category, 'sports_summary')
        articles = get_articles_from_supabase(table)
        return jsonify({'articles': articles})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
