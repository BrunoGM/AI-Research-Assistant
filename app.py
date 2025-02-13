from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import time
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import validators

load_dotenv()

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def search_web(query):
    ddg_url = "https://html.duckduckgo.com/html/"
    params = {
        "q": query,
        "kl": "wt-wt",
        "kp": "-2"
    }
    try:
        response = requests.post(ddg_url, 
            data=params,
            headers={'User-Agent': headers['User-Agent']},
            timeout=10
        )
        soup = BeautifulSoup(response.text, 'lxml')
        results = soup.find_all('a', class_='result__url', href=True)
        return [result['href'] for result in results[:3] if validators.url(result['href'])]
    except Exception as e:
        print(f"Search error: {e}")
        return []

def get_page_content(url):
    """Extract main content from webpage with improved targeting."""
    try:
        time.sleep(1)  # Respect crawl delay
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'iframe', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
            
        # Try to find main content
        main_content = None
        
        # Look for common content containers
        content_tags = [
            soup.find('article'),
            soup.find('main'),
            soup.find(class_=lambda x: x and any(term in str(x).lower() for term in ['content', 'article', 'post', 'entry'])),
            soup.find(id=lambda x: x and any(term in str(x).lower() for term in ['content', 'article', 'post', 'entry']))
        ]
        
        # Use the first valid content container found
        for content in content_tags:
            if content:
                main_content = content
                break
                
        # If no specific container found, use body
        if not main_content:
            main_content = soup.find('body')
            
        if main_content:
            # Get text while preserving some structure
            paragraphs = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
            text = '\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        else:
            text = soup.get_text(strip=True)
            
        # Clean up the text
        text = ' '.join(text.split())  # Remove extra whitespace
        
        # Take first 5000 characters (increased from 2000)
        return f"From {url}:\n{text[:5000]}"
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return ""

def is_valid_query(query):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,?!-:;'\"()")
    return all(c in allowed_chars for c in query) and len(query) <= 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
@limiter.limit("10/minute")
def search():
    try:
        query = request.form['query']
        
        if not is_valid_query(query):
            return render_template('error.html', 
                message="Invalid query characters or length")
        
        urls = search_web(query)
        if not urls:
            return render_template('index.html', 
                response="No search results found. Please try a different query.")
            
        context = "\n".join([get_page_content(url) for url in urls if url])
        if not context.strip():
            return render_template('index.html', 
                response="Could not extract content from search results. Please try again.")
            
        # Modified prompt to handle longer content
        response = model.generate_content(
            f"Using the following web content, provide a comprehensive answer:\n\n{context}\n\n"
            f"Query: {query}\n\n"
            "Format your response with exactly these sections:\n\n"
            "## Answer\n"
            "(your detailed answer here)\n\n"
            "## Sources\n"
            "(list each source URL on a new line)\n\n"
            "## Related Questions\n"
            "- (related question 1)\n"
            "- (related question 2)\n"
            "- (related question 3)"
        )
        
        # Ensure consistent newlines and section spacing
        formatted_response = response.text.replace('\r\n', '\n').strip()
        
        # Ensure each section has proper spacing
        formatted_response = formatted_response.replace('\n## ', '\n\n## ')
        
        return render_template('index.html', response=formatted_response)
    except Exception as e:
        print(f"Search error: {str(e)}")
        return render_template('error.html', message=str(e))

@app.route('/debug')
def debug():
    test_url = "https://www.healthline.com/nutrition/fish-oil-benefits"
    return get_page_content(test_url)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', message="Internal server error"), 500

if __name__ == '__main__':
    app.run(debug=True)
