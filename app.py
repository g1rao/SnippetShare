import sqlite3
import os
from flask import Flask, jsonify, request, send_from_directory, g

# --- App Configuration ---
app = Flask(__name__, static_folder='.', static_url_path='')
app.config['DATABASE'] = 'snippets.db'
app.config['SECRET_KEY'] = 'your_super_secret_key' # Change this in production

# --- Database Helper Functions ---

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """Closes the database again at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database schema."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print("Initialized the database.")

@app.cli.command('init-db')
def init_db_command():
    """Creates the database tables."""
    # Check if DB exists, if so, ask for confirmation to avoid accidental data loss
    if os.path.exists(app.config['DATABASE']):
        response = input(f"Database '{app.config['DATABASE']}' already exists. Re-initializing will delete all data. Continue? [y/N]: ")
        if response.lower() != 'y':
            print("Database initialization cancelled.")
            return
        os.remove(app.config['DATABASE'])

    init_db()


# --- API Routes ---

@app.route('/api/snippets', methods=['GET'])
def get_all_snippets():
    """Fetches all snippets from the database."""
    db = get_db()
    snippets = db.execute('SELECT id, content, created_at FROM snippets ORDER BY created_at DESC').fetchall()
    return jsonify([dict(snippet) for snippet in snippets])

@app.route('/api/snippets/<int:snippet_id>', methods=['GET'])
def get_snippet(snippet_id):
    """Fetches a single snippet by its ID."""
    db = get_db()
    snippet = db.execute('SELECT id, content, created_at FROM snippets WHERE id = ?', (snippet_id,)).fetchone()
    if snippet is None:
        return jsonify({'error': 'Snippet not found'}), 404
    return jsonify(dict(snippet))

@app.route('/api/snippets', methods=['POST'])
def create_snippet():
    """Creates a new snippet."""
    if not request.json or 'content' not in request.json:
        return jsonify({'error': 'Missing content'}), 400
    
    content = request.json['content']
    db = get_db()
    cursor = db.execute('INSERT INTO snippets (content) VALUES (?)', (content,))
    db.commit()
    
    new_snippet_id = cursor.lastrowid
    return jsonify({'id': new_snippet_id, 'message': 'Snippet created successfully'}), 201

# --- Frontend Serving ---

@app.route('/')
def index():
    """Serves the main index.html file."""
    return send_from_directory('.', 'index.html')

@app.errorhandler(404)
def not_found(e):
    """Handles 404s by serving index.html for client-side routing."""
    # This ensures that refreshing a page like /?id=123 still works
    return send_from_directory('.', 'index.html')


# --- Main Entry Point ---
if __name__ == '__main__':
    # Check if the database exists. If not, initialize it.
    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            print("Database not found. Initializing...")
            init_db()
    
    app.run(host='0.0.0.0', debug=True, port=8000)
