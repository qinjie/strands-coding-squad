# Functional Specification

## System Overview
Flask application that fetches Singapore news from NewsAPI and displays it with filtering capabilities.

## Functional Requirements
1. **News Feed**: Display 20 latest articles with pagination
2. **Article Details**: Clickable articles showing full content
3. **Category Filter**: Dropdown with NewsAPI categories
4. **Caching**: Cache API responses for 15 minutes

## Non-functional Requirements
- Load time < 2 seconds
- 99.9% uptime SLA
- Responsive design for mobile/desktop

## API Integration
- NewsAPI v2 endpoint: /top-headlines?country=sg
- Error handling for 429/500 responses
- Rate limiting: 100 requests/day
