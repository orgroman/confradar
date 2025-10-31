## Epic
Backend Infrastructure & Data Pipeline

## Description
Build a REST API using FastAPI to serve conference data to the frontend application. This API will provide endpoints for listing, searching, and retrieving conference details.

## Background
The frontend application (issues #86-#125, milestones FE-1 through FE-5) requires a backend API to:
- Fetch paginated lists of conferences
- Search and filter conferences by multiple criteria
- Retrieve detailed information for individual conferences
- Support timezone conversions and calendar export

## API Endpoints

### Core Endpoints
- `GET /api/conferences` - List conferences with pagination, filtering, sorting
- `GET /api/conferences/{id}` - Get conference details
- `GET /api/conferences/search` - Full-text search
- `GET /api/deadlines/upcoming` - Upcoming deadlines (next 30/60/90 days)
- `GET /api/health` - Health check endpoint

### Filtering Parameters
- `field` - Filter by research field (NLP, CV, ML, etc.)
- `location` - Filter by location/region
- `year` - Filter by conference year
- `deadline_start` / `deadline_end` - Date range for deadlines
- `sort` - Sort by deadline, name, date
- `page` / `limit` - Pagination

### Response Format
```json
{
  "conferences": [...],
  "total": 250,
  "page": 1,
  "limit": 20,
  "has_more": true
}
```

## Tasks

### FastAPI Setup
- [ ] Create FastAPI application structure
- [ ] Add CORS middleware for frontend access
- [ ] Configure logging and error handling
- [ ] Add Swagger/OpenAPI documentation
- [ ] Set up development server with hot reload

### Database Integration
- [ ] Create SQLAlchemy query builders for filtering
- [ ] Implement pagination with cursor or offset
- [ ] Add database connection pooling
- [ ] Optimize queries with proper indexes
- [ ] Add query result caching (Redis optional)

### Endpoints Implementation
- [ ] Implement `/conferences` list endpoint with all filters
- [ ] Implement `/conferences/{id}` detail endpoint
- [ ] Implement `/search` full-text search
- [ ] Implement `/deadlines/upcoming` endpoint
- [ ] Add `/health` and `/metrics` endpoints

### API Features
- [ ] Add request validation with Pydantic models
- [ ] Implement rate limiting (per-IP quotas)
- [ ] Add ETag support for caching
- [ ] Add compression (gzip)
- [ ] Implement CORS with configurable origins

### Documentation
- [ ] Generate OpenAPI schema
- [ ] Add endpoint descriptions and examples
- [ ] Document authentication (if needed)
- [ ] Create API usage guide
- [ ] Add rate limit documentation

### Testing
- [ ] Unit tests for endpoint handlers
- [ ] Integration tests with test database
- [ ] Load testing (concurrent requests)
- [ ] API contract testing

## Acceptance Criteria
- [ ] All endpoints documented in Swagger UI
- [ ] Pagination works correctly with large datasets
- [ ] Filtering returns correct results
- [ ] Response times <200ms for list queries
- [ ] CORS configured for frontend domain
- [ ] API tested with >1000 conferences
- [ ] Rate limiting prevents abuse

## Technology Stack
- **Framework**: FastAPI 0.104+
- **Database**: SQLAlchemy with PostgreSQL
- **Validation**: Pydantic v2
- **CORS**: fastapi.middleware.cors
- **Testing**: pytest + httpx
- **Documentation**: OpenAPI (built-in)

## Priority
P1 - Required for frontend application (FE-4: API Integration milestone)

## Estimated Effort
5-7 days

## Related Issues
- Frontend Epic: #86
- API Integration Epic: #94
- Frontend issues requiring API: #119, #120, #121, #122, #123

## Deployment Notes
- API should run on separate port from Dagster (e.g., 8000)
- Consider FastAPI deployment options: Uvicorn, Gunicorn + Uvicorn workers
- Add to docker-compose.yml for local development
- Document environment variables (DATABASE_URL, CORS_ORIGINS, etc.)

## Future Enhancements
- Authentication with API keys
- GraphQL endpoint (alternative to REST)
- WebSocket for real-time updates
- Export endpoints (.ics, .json, .csv)
