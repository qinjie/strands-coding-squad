from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
import logging
from src.app.api import get_top_headlines, search_news, NewsAPIException
from src.app.models import Article

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/category/<string:category>')
def index(category=None):
    """
    Main route to display news articles, optionally filtered by category
    """
    page = request.args.get('page', 1, type=int)
    
    try:
        # Get news data from API
        news_data = get_top_headlines(category, page)
        
        # Process articles
        articles = []
        if news_data.get('status') == 'ok':
            for article_data in news_data.get('articles', []):
                articles.append(Article(article_data))
                
        # Get total results and pages
        total_results = news_data.get('totalResults', 0)
        total_pages = (total_results + current_app.config['NEWS_PAGE_SIZE'] - 1) // current_app.config['NEWS_PAGE_SIZE']
        
        return render_template('index.html', 
                              articles=articles,
                              category=category or 'all',
                              categories=current_app.config['NEWS_CATEGORIES'],
                              page=page,
                              total_pages=total_pages)
    
    except NewsAPIException as e:
        logger.error(f"API error: {str(e)}")
        flash(f"Error fetching news: {str(e)}", "danger")
        return render_template('error.html', error=str(e)), 500

@main.route('/search')
def search():
    """
    Search for news articles based on query
    """
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return redirect(url_for('main.index'))
    
    try:
        # Get search results from API
        search_data = search_news(query, page)
        
        # Process articles
        articles = []
        if search_data.get('status') == 'ok':
            for article_data in search_data.get('articles', []):
                articles.append(Article(article_data))
                
        # Get total results and pages
        total_results = search_data.get('totalResults', 0)
        total_pages = (total_results + current_app.config['NEWS_PAGE_SIZE'] - 1) // current_app.config['NEWS_PAGE_SIZE']
        
        return render_template('search.html', 
                              articles=articles,
                              query=query,
                              page=page,
                              total_pages=total_pages)
    
    except NewsAPIException as e:
        logger.error(f"API error: {str(e)}")
        flash(f"Error searching news: {str(e)}", "danger")
        return render_template('error.html', error=str(e)), 500

@main.route('/article')
def article():
    """
    Display a single article based on URL parameters
    
    Note: Since NewsAPI doesn't provide a direct endpoint to get a single article by ID,
    we pass all article details as URL parameters
    """
    title = request.args.get('title')
    url = request.args.get('url')
    
    if not url:
        abort(404)
    
    # Create an article object from request parameters
    article_data = {
        'source': {
            'id': request.args.get('source_id'),
            'name': request.args.get('source_name')
        },
        'author': request.args.get('author'),
        'title': title,
        'description': request.args.get('description'),
        'url': url,
        'urlToImage': request.args.get('url_to_image'),
        'publishedAt': request.args.get('published_at'),
        'content': request.args.get('content')
    }
    
    article = Article(article_data)
    return render_template('article.html', article=article)

@main.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page not found"), 404

@main.errorhandler(500)
def server_error(e):
    return render_template('error.html', error="Server error"), 500