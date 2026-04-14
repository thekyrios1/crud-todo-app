# Tasks — A Refined Todo Application

A full-stack CRUD application for personal task management, featuring a production-grade Vue.js 3 frontend and FastAPI backend. Designed with professional aesthetics inspired by Bear and Craft—typography-driven, deliberately restrained, and focused on clarity over decoration.

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Vue 3 (Composition API) + Vite | Reactive UI framework |
| State Management | Pinia | Store management |
| Utilities | VueUse | Theme toggle, composables |
| Routing | Vue Router | Navigation |
| Backend | FastAPI | REST API server |
| Database ORM | SQLAlchemy | Database operations |
| Data Validation | Pydantic | Request/response validation |
| Database | SQLite | Lightweight file-based storage |

## Design Philosophy

This application embodies **professional refinement**: typography-first design with EB Garamond for headings, subtle animations using exponential easing, and dual light/dark themes built with OKLCH color space for perceptual consistency.

**Key design principles:**
- Typography carries visual weight; minimal decorative elements
- Generous whitespace creates breathing room
- Progressive disclosure—hover reveals secondary actions
- Smooth theme switching between carefully tuned light and dark modes

## Project Structure

```
CRUDapp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application & routes
│   │   ├── database.py          # SQLite connection setup
│   │   ├── models.py            # SQLAlchemy Todo model
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   └── crud.py              # CRUD operation functions
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Configuration (DB path)
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   └── TodoForm.vue     # Create/Edit form component
│   │   ├── views/
│   │   │   └── TodoList.vue     # Main list view with CRUD actions
│   │   ├── stores/
│   │   │   └── todoStore.js     # Pinia store for todos
│   │   ├── router.js            # Vue Router configuration
│   │   ├── api.js               # API service layer
│   │   ├── App.vue              # Root component
│   │   └── main.js              # Application entry point
│   ├── index.html
│   ├── package.json             # npm dependencies
│   └── vite.config.js           # Vite configuration
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## Database Schema (SQLite)

### Table: todos

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| title | TEXT | NOT NULL | Todo title (max 200 chars) |
| description | TEXT | Nullable | Detailed description |
| completed | BOOLEAN | DEFAULT FALSE | Completion status |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

## API Endpoints (FastAPI)

### 1. Create Todo - `POST /todos`

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response:** Created todo object with generated id and timestamps (201 status)

### 2. Get All Todos - `GET /todos`

**Query Parameters (optional):**
- `completed`: filter by status (true/false)
- `limit`: max results to return
- `offset`: pagination offset

**Response:** Array of todo objects (200 status)

### 3. Get Single Todo - `GET /todos/{id}`

**Path Parameter:** id (integer)

**Response:** Single todo object or 404 if not found

### 4. Update Todo - `PUT /todos/{id}`

**Path Parameter:** id (integer)

**Request Body:** Updated fields (title, description, completed)

**Response:** Updated todo object or 404 if not found

### 5. Delete Todo - `DELETE /todos/{id}`

**Path Parameter:** id (integer)

**Response:** Success message or 404 if not found

## Frontend Components Design

### TodoList.vue
- Displays list of all todos in a table/list format
- Shows: title, description preview, completion status, timestamps
- Actions per row: Edit button, Delete button, Toggle complete checkbox
- Search/filter input for filtering by title or status
- Pagination controls (if needed)

### TodoForm.vue
- Form fields: Title (required), Description (optional), Completed (checkbox)
- Validation: Title required, max length checks
- Submit action: Creates new todo OR updates existing based on mode
- Cancel button: Clears form and returns to list

### Pinia Store (todoStore.js)

**State:**
- `todos`: Array of all todos
- `loading`: Boolean for loading state
- `error`: Error message if any

**Actions:**
- `fetchTodos()`: GET /todos
- `createTodo(data)`: POST /todos
- `updateTodo(id, data)`: PUT /todos/{id}
- `deleteTodo(id)`: DELETE /todos/{id}
- `toggleComplete(id)`: Toggle completed status

## Dependencies

### Backend (requirements.txt)
```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.25
pydantic>=2.5.3
python-dotenv>=1.0.0
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "vue": "^3.4.0",
    "pinia": "^2.1.7",
    "vue-router": "^4.2.5",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.3",
    "vite": "^5.0.0"
  }
}
```

## Quick Start

### Run the Application (Already Set Up)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

### Fresh Setup

If you cloned this repository and need to set it up from scratch:

## Getting Started

### Prerequisites
- Python 3.9+ 
- Node.js 18+ and npm

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate virtual environment:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure `.env` file (create if not exists):
   ```
   DATABASE_URL=sqlite:///./todos.db
   ```

6. Run the server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure API base URL in `src/api.js`:
   ```javascript
   const API_BASE = 'http://localhost:8000'
   ```

4. Run dev server:
   ```bash
   npm run dev
   ```

### Development Flow

- Backend runs on http://localhost:8000
- Frontend runs on http://localhost:5173 (or port specified by Vite)
- Frontend makes API calls to backend via axios
- SQLite database file created in backend directory

## Implementation Order (Recommended)

### Phase 1 - Backend Foundation
1. Set up project structure and dependencies
2. Create `database.py` with SQLite connection
3. Define `models.py` with Todo model
4. Create `schemas.py` with Pydantic validators
5. Implement CRUD functions in `crud.py`
6. Build `main.py` with API routes

### Phase 2 - Backend Testing
7. Test all endpoints using curl or Postman
8. Verify database persistence and data integrity

### Phase 3 - Frontend Foundation
9. Initialize Vue project with Vite
10. Install Pinia, Vue Router, Axios
11. Create `api.js` service layer
12. Build `todoStore.js` Pinia store

### Phase 4 - Frontend UI
13. Create `TodoForm.vue` component
14. Build `TodoList.vue` view
15. Set up `router.js` with routes
16. Style components with CSS

### Phase 5 - Integration & Polish
17. Connect frontend to backend API
18. Add loading states and error handling
19. Implement form validation
20. Test full CRUD workflow end-to-end

## Key Design Decisions & Tradeoffs

| Decision | Rationale | Alternative Considered |
|----------|-----------|----------------------|
| SQLite over PostgreSQL | Simpler setup, no server needed for development | PostgreSQL would be better for production scalability |
| FastAPI over Flask | Built-in validation, auto docs, async support | Flask is simpler but requires more boilerplate |
| Vue 3 Composition API | Better code organization, TypeScript friendly | Options API is more familiar to Vue 2 users |
| Pinia over Vuex | Simpler API, better TypeScript support | Vuex has larger ecosystem |
| Vite over Vue CLI | Faster HMR, smaller bundle sizes | Vue CLI has more plugins available |

## Potential Enhancements (Future)

- User authentication and authorization
- Categories/tags for todos
- Due dates and reminders
- File attachments to todos
- Export/import functionality
- Real-time updates with WebSockets
- Mobile responsive design improvements
- Dark mode theme toggle

## API Documentation

When the backend is running, interactive API documentation is automatically available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT License - Feel free to use this project for learning and development.
