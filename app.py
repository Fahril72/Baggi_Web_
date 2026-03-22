from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    """Menginisialisasi database SQLite berdasarkan data dari data_kota.sql"""
    conn = sqlite3.connect('seattle.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_kota (
            Id INTEGER PRIMARY KEY,
            Nama_kota TEXT NOT NULL,
            Negara TEXT NOT NULL,
            Negara_Bagian TEXT NOT NULL,
            Bahasa TEXT NOT NULL,
            Julukan TEXT NOT NULL,
            Tahun_berdiri INTEGER NOT NULL,
            Mata_uang TEXT NOT NULL,
            AsalUsul_Nama TEXT NOT NULL,
            Populasi TEXT NOT NULL,
            Suku_Asli TEXT NOT NULL,
            Luas_kota TEXT NOT NULL,
            Olahraga_Favorit TEXT NOT NULL,
            Tempat_wisata TEXT NOT NULL,
            Walikota TEXT NOT NULL,
            Mata_pencaharian TEXT NOT NULL,
            Iklim TEXT NOT NULL
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM data_kota")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO data_kota VALUES (
                1, 'Seattle', 'Amerika Serikat', 'Washington', 'Bahasa Inggris', 
                'Kota zamrud(ZamrudCiy), Kota hujan(RainCity), Kota jet(JetCity)', 1851, 
                'Dolar Amerika Serikat(USD)', "Nama kepala suku(Chief) Si'ahl (shealth)", 
                '755.000 - 816.600 Jiwa pada tahun 2025', 
                'Suku Duwamish, Suquamish, Coast Salish, dan Muckleshoot', '392,2 Km', 
                'Sepak bola, sepak bola amerika, dan bisbol', 
                'Space needle, museum of pop culture, kery park, Gum wall, dan pike place market', 
                'Katie Wilson pada tahun 2026', 
                'Sektor teknologi, manufaktur, dan layanan kesehatan/bioteknologi', 
                'Sedang hingga mediterania'
            )
        ''')
    conn.commit()
    conn.close()

def bfs_search(query, data_list):
    """
    Algoritma Breadth-First Search untuk mencari kecocokan query 
    di dalam list data kota.
    """
    queue = data_list.copy()
    results = []
    
    while queue:
        current_node = queue.pop(0)
        combined_text = " ".join(str(value).lower() for value in current_node.values())
        
        if query.lower() in combined_text:
            results.append(current_node)
            
    return results

COMMON_CSS = """
*, html, body {
    margin: 0; padding: 0; box-sizing: border-box; text-decoration: none;
    font-family: system-ui, -apple-system, sans-serif;
    background-color: #2C2C2C;
}
body { display: flex; flex-direction: column; min-height: 100vh; color: white; }
header { display: flex; justify-content: end; align-items: center; height: 50px; width: 100%; }
.header-right { display: flex; padding: 10px 20px; }
.header-right a { margin-right: 10px; color: blanchedalmond; }
section { display: flex; justify-content: center; height: 100%; }
.feature { display: flex; flex-direction: column; align-items: center; width: 100%; margin-top: 50px; } 
.google-style { font-size: 90px; letter-spacing: -10px; color: blanchedalmond; margin-bottom: 20px; }
.search { display: flex; flex-direction: column; padding: 20px; width: 80%; max-width: 600px; gap: 20px; }
.search-input { 
    display: flex; align-items: center; width: 100%; border: 1px solid blanchedalmond; 
    padding: 0 16px; border-radius: 99px; color: blanchedalmond; 
}
.search-input input { 
    flex: 1; font-size: 15px; padding: 12px; border: none; outline: none; color: white; background: transparent; 
}
.search-action { display: flex; justify-content: center; gap: 12px; }
.search-action button { 
    border: 1px solid blanchedalmond; color: white; padding: 8px 16px; 
    border-radius: 6px; cursor: pointer; background: transparent; 
}
.results-container { width: 80%; max-width: 800px; margin: 20px auto; padding: 20px; }
.result-item { margin-bottom: 30px; padding: 20px; border-bottom: 1px solid rgba(255,235,205,0.3); }
.result-title { font-size: 24px; color: blanchedalmond; margin-bottom: 5px; }
.result-category { font-size: 14px; color: #aaa; margin-bottom: 10px; }
.detail-grid { display: grid; grid-template-columns: 150px 1fr; gap: 10px; font-size: 14px; }
.label { color: blanchedalmond; font-weight: bold; }
"""

@app.route('/')
def index():
    return render_template_string("""
    <html>
    <head>
        <style>{{ css|safe }}</style>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    </head>
    <body>
        <header>
            <div class="header-right">
                <a href="#"><span class="material-icons">account_circle</span></a>
                <a href="#"><span class="material-icons">queue_music</span></a>
                <a href="#"><span class="material-icons">more_vert</span></a>
            </div>
        </header>
        <section>
            <div class="feature">
                 <h1 class="google-style">Baggi</h1>
                <div class="search">
                    <form action="/search" method="GET" class="search-input">
                        <span class="material-icons">search</span>
                        <input name="q" placeholder="Cari Seattle..."/>
                        <span class="material-icons">keyboard_voice</span>
                    </form>
                    <div class="search-action">
                        <button onclick="document.forms[0].submit()">Baggi search</button>
                        <button>About Baggi</button>
                    </div>
                </div>
            </div>
        </section>
    </body>
    </html>
    """, css=COMMON_CSS)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('index'))

    conn = sqlite3.connect('seattle.db')
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM data_kota").fetchall()
    conn.close()
    
    data_list = [dict(row) for row in rows]
    
    results = bfs_search(query, data_list)

    return render_template_string("""
    <html>
    <head>
        <style>{{ css|safe }}</style>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    </head>
    <body>
        <header>
            <div class="header-right"><a href="/">Home</a></div>
        </header>
        <div class="results-container">
            <h2 style="color: blanchedalmond;">Hasil pencarian untuk: "{{ query }}"</h2>
            <hr style="border: 0.5px solid #444; margin: 20px 0;">
            
            {% if results %}
                {% for item in results %}
                <div class="result-item">
                    <div class="result-category">{{ item.Negara }} &bull; {{ item.Negara_Bagian }}</div>
                    <div class="result-title">{{ item.Nama_kota }}</div>
                    <p style="font-style: italic; color: #ccc; margin-bottom: 15px;">"{{ item.Julukan }}"</p>
                    
                    <div class="detail-grid">
                        <div class="label">Walikota:</div><div>{{ item.Walikota }}</div>
                        <div class="label">Populasi:</div><div>{{ item.Populasi }}</div>
                        <div class="label">Wisata:</div><div>{{ item.Tempat_wisata }}</div>
                        <div class="label">Ekonomi:</div><div>{{ item.Mata_pencaharian }}</div>
                        <div class="label">Iklim:</div><div>{{ item.Iklim }}</div>
                        <div class="label">Suku Asli:</div><div>{{ item.Suku_Asli }}</div>
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <p>Data tidak ditemukan dalam basis data Baggi.</p>
            {% endif %}
        </div>
    </body>
    </html>
    """, css=COMMON_CSS, results=results, query=query)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)