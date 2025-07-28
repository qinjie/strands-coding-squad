# Database Schema and Data Flow - Singapore News Flask Application

## Overview

This document outlines the database schema and data flow for the Singapore News Flask application. While the primary data source is the NewsAPI, we'll maintain a lightweight database for caching, user preferences, and analytics.

## Database Technology Selection

For this application, we recommend:

- **Development**: SQLite (for simplicity)
- **Production**: PostgreSQL (for robustness and concurrent access)

The application will use SQLAlchemy ORM with Flask-SQLAlchemy extension to abstract the database interactions, making it easy to switch between database engines.

## Schema Design

### Entity-Relationship Diagram

```
┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
│     Category      │       │   CachedArticle   │       │    UserActivity   │
├───────────────────┤       ├───────────────────┤       ├───────────────────┤
│ id (PK)           │       │ id (PK)           │       │ id (PK)           │
│ name              │◄──────┤ category_id (FK)  │       │ session_id        │
│ description       │       │ title             │       │ article_id (FK)   │
└───────────────────┘       │ description       │       │ activity_type     │
                            │ content           │       │ timestamp         │
                            │ source_id         │       └───────────────────┘
                            │ source_name       │               ▲
                            │ author            │               │
                            │ url               │               │
                            │ image_url         │               │
                            │ published_at      │◄──────────────┘
                            │ cached_at         │
                            │ expires_at        │
                            └───────────────────┘
                                     ▲
                                     │
                            ┌────────┴──────────┐
                            │   ArticleTag      │
                            ├───────────────────┤
                            │ article_id (FK,PK)│
                            │ tag_id (FK,PK)    │
                            └───────────────────┘
                                     │
                                     ▼
                            ┌───────────────────┐
                            │       Tag         │
                            ├───────────────────┤
                            │ id (PK)           │
                            │ name              │
                            └───────────────────┘
```

### Table Definitions

#### Category

Stores news categories for filtering.

| Column      | Type         | Constraints       | Description                   |
|-------------|--------------|-------------------|-------------------------------|
| id          | INTEGER      | PK, AUTO INCREMENT| Unique identifier             |
| name        | VARCHAR(50)  | NOT NULL, UNIQUE  | Category name (e.g., Business)|
| description | VARCHAR(255) |                   | Category description          |

#### CachedArticle

Stores cached news articles from NewsAPI.

| Column       | Type         | Constraints       | Description                   |
|--------------|--------------|-------------------|-------------------------------|
| id           | VARCHAR(100) | PK               | Unique identifier (from API)  |
| category_id  | INTEGER      | FK               | Reference to Category         |
| title        | VARCHAR(255) | NOT NULL         | Article title                 |
| description  | TEXT         |                  | Article description           |
| content      | TEXT         |                  | Article content               |
| source_id    | VARCHAR(100) |                  | Source identifier             |
| source_name  | VARCHAR(100) |                  | Source name                   |
| author       | VARCHAR(100) |                  | Article author                |
| url          | VARCHAR(500) | NOT NULL         | Original article URL          |
| image_url    | VARCHAR(500) |                  | Article image URL             |
| published_at | TIMESTAMP    | NOT NULL         | Publication timestamp         |
| cached_at    | TIMESTAMP    | NOT NULL         | When article was cached       |
| expires_at   | TIMESTAMP    | NOT NULL         | When cache expires            |

#### Tag

Stores tags for categorizing articles beyond main categories.

| Column | Type        | Constraints       | Description                   |
|--------|-------------|-------------------|-------------------------------|
| id     | INTEGER     | PK, AUTO INCREMENT| Unique identifier             |
| name   | VARCHAR(50) | NOT NULL, UNIQUE  | Tag name                      |

#### ArticleTag

Junction table for many-to-many relationship between articles and tags.

| Column     | Type         | Constraints       | Description                   |
|------------|--------------|-------------------|-------------------------------|
| article_id | VARCHAR(100) | PK, FK           | Reference to CachedArticle    |
| tag_id     | INTEGER      | PK, FK           | Reference to Tag              |

#### UserActivity

Tracks user interactions with articles for analytics.

| Column        | Type         | Constraints       | Description                   |
|---------------|--------------|-------------------|-------------------------------|
| id            | INTEGER      | PK, AUTO INCREMENT| Unique identifier             |
| session_id    | VARCHAR(100) | NOT NULL         | Anonymous session identifier  |
| article_id    | VARCHAR(100) | FK               | Reference to CachedArticle    |
| activity_type | VARCHAR(50)  | NOT NULL         | Type of activity (view, share)|
| timestamp     | TIMESTAMP    | NOT NULL         | When activity occurred        |

### Indexes

| Table         | Index Name              | Columns                    | Type    | Purpose                                |
|---------------|-------------------------|----------------------------|---------|----------------------------------------|
| CachedArticle | idx_article_category    | category_id                | BTREE   | Fast filtering by category             |
| CachedArticle | idx_article_published   | published_at               | BTREE   | Sorting by publication date            |
| CachedArticle | idx_article_expiration  | expires_at                 | BTREE   | Cache expiration management            |
| UserActivity  | idx_activity_session    | session_id                 | BTREE   | Grouping activities by session         |
| UserActivity  | idx_activity_article    | article_id                 | BTREE   | Finding activities for specific article|
| UserActivity  | idx_activity_timestamp  | timestamp                  | BTREE   | Time-based analytics                   |

## Data Flow Diagrams

### Article Caching Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  User Request │────►│ Check Cache  │────►│ Cache Miss?  │─Yes─►│ Fetch from  │
└──────────────┘     └──────────────┘     └──────┬───────┘     │   NewsAPI    │
                                                 │             └───────┬──────┘
                                                 No                    │
                                                 │                     │
                                          ┌──────▼───────┐     ┌───────▼──────┐
                                          │ Return Cached│     │ Store in     │
                                          │    Data      │◄────┤ Database     │
                                          └──────────────┘     └──────────────┘
```

### User Activity Tracking Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  User Views   │────►│ Log Activity │────►│  Store in    │
│   Article     │     │              │     │  Database    │
└──────────────┘     └──────────────┘     └──────────────┘
```

## Data Access Patterns

### Object-Relational Mapping (ORM)

The application will use SQLAlchemy ORM to interact with the database. Example model definitions:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    articles = db.relationship('CachedArticle', backref='category', lazy=True)

class CachedArticle(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    source_id = db.Column(db.String(100))
    source_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    url = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500))
    published_at = db.Column(db.DateTime, nullable=False)
    cached_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    tags = db.relationship('Tag', secondary='article_tag', lazy='subquery',
                          backref=db.backref('articles', lazy=True))
    activities = db.relationship('UserActivity', backref='article', lazy=True)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

article_tag = db.Table('article_tag',
    db.Column('article_id', db.String(100), db.ForeignKey('cached_article.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    article_id = db.Column(db.String(100), db.ForeignKey('cached_article.id'))
    activity_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
```

### Repository Pattern

The application will implement a repository pattern to abstract database operations:

```python
class ArticleRepository:
    def get_latest_articles(self, category=None, limit=20, offset=0):
        query = CachedArticle.query.order_by(CachedArticle.published_at.desc())
        
        if category:
            query = query.filter_by(category_id=category)
            
        return query.limit(limit).offset(offset).all()
    
    def get_article_by_id(self, article_id):
        return CachedArticle.query.get(article_id)
    
    def save_article(self, article):
        db.session.add(article)
        db.session.commit()
        
    def get_expired_articles(self):
        return CachedArticle.query.filter(CachedArticle.expires_at < datetime.utcnow()).all()
```

## Data Migration Strategy

The application will use Alembic (via Flask-Migrate) for database migrations:

1. **Initial Schema Creation**: Define base schema in SQLAlchemy models
2. **Version Control**: Track schema changes in version control
3. **Migration Scripts**: Generate migration scripts for schema changes
4. **Deployment**: Apply migrations during deployment process

## Data Backup and Recovery

For production environments:

1. **Regular Backups**: Daily database backups
2. **Point-in-Time Recovery**: Transaction log backups
3. **Backup Verification**: Regular testing of backup restoration
4. **Disaster Recovery Plan**: Documented procedures for data recovery

## Data Retention Policy

1. **Cached Articles**: Retain for 30 days after expiration
2. **User Activity Data**: Retain for 90 days
3. **Aggregated Analytics**: Retain indefinitely (anonymized)

## Performance Considerations

1. **Connection Pooling**: Configure appropriate connection pool size
2. **Query Optimization**: Use indexes for common query patterns
3. **Batch Processing**: Bulk operations for efficiency
4. **Pagination**: Limit result sets for better performance
5. **Lazy Loading**: Configure appropriate lazy loading strategies for relationships