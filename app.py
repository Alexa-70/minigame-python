import random
from flask import Flask, render_template_string, request, session

app = Flask(__name__)
# Cheie secretă necesară pentru a păstra numărul jocului în memorie
app.secret_key = "cheie_secreta_pentru_joc"

UTILIZATOR_CORECT = "admin"
PAROLA_CORECTA = "1234"

PAGINA_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Platforma mea Web</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #1e1e2e; color: #ffffff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background-color: #252538; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); width: 350px; text-align: center; }
        h2 { margin-bottom: 20px; color: #a3a3ff; }
        input[type="text"], input[type="password"], input[type="number"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #444465; border-radius: 5px; background-color: #1e1e2e; color: #fff; box-sizing: border-box; }
        button, .btn-link { display: block; width: 100%; padding: 12px; background-color: #5865f2; border: none; border-radius: 5px; color: white; font-weight: bold; cursor: pointer; margin-top: 10px; text-decoration: none; box-sizing: border-box; }
        button:hover, .btn-link:hover { background-color: #4752c4; }
        .mesaj { margin-top: 15px; font-weight: bold; padding: 10px; border-radius: 5px; }
        .eroare { background-color: #f23f43; color: white; }
        .sugestie { background-color: #e9a115; color: black; }
        .succes { background-color: #23a55a; color: white; }
    </style>
</head>
<body>
    <div class="card">
        {% if not session.get('autentificat') %}
            <!-- ECRAN DE LOGIN -->
            <h2>Autentificare</h2>
            <form method="POST" action="/">
                <input type="text" name="username" placeholder="Nume utilizator" required autocomplete="off">
                <input type="password" name="password" placeholder="Parolă" required>
                <button type="submit">Conectare</button>
            </form>
            {% if eroare %}
                <div class="mesaj eroare">{{ eroare }}</div>
            {% endif %}
        {% else %}
            <!-- ECRAN DE JOC (MINIGAME) -->
            <h2>Ghicește Numărul! 🎯</h2>
            <p>Calculatorul a ales un număr între 1 și 100. Încearcă să îl ghicești!</p>
            
            <form method="POST" action="/joaca">
                <input type="number" name="ghicit" placeholder="Introdu un număr" min="1" max="100" required autocomplete="off">
                <button type="submit">Trimite</button>
            </form>

            {% if indiciu %}
                <div class="mesaj {% if 'Felicitări' in indiciu %}succes{% else %}sugestie{% endif %}">
                    {{ indiciu }}
                </div>
            {% endif %}
            
            <p style="margin-top: 15px; color: #bbb;">Încercări curente: <strong>{{ session.get('incercari', 0) }}</strong></p>
            <a href="/reset" class="btn-link" style="background-color: #4f545c;">Resetează Jocul</a>
            <a href="/logout" class="btn-link" style="background-color: #f23f43; margin-top: 5px;">Ieși din cont</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    eroare = None
    if request.method == "POST":
        user = request.form.get("username")
        parola = request.form.get("password")
        
        if user == UTILIZATOR_CORECT and parola == PAROLA_CORECTA:
            session['autentificat'] = True
            # Inițializăm starea jocului
            session['numar_secret'] = random.randint(1, 100)
            session['incercari'] = 0
        else:
            eroare = "Utilizator sau parolă incorectă!"
            
    return render_template_string(PAGINA_HTML, eroare=eroare)

@app.route("/joaca", methods=["POST"])
def joaca():
    if not session.get('autentificat'):
        return index()
        
    ghicit = int(request.form.get("ghicit"))
    session['incercari'] = session.get('incercari', 0) + 1
    numar_secret = session.get('numar_secret')
    
    if ghicit < numar_secret:
        indiciu = f"Prea MIC! Încearcă un număr mai mare decât {ghicit}."
    elif ghicit > numar_secret:
        indiciu = f"Prea MARE! Încearcă un număr mai mic decât {ghicit}."
    else:
        indiciu = f"🎉 Felicitări! Ai ghicit numărul {numar_secret} din {session['incercari']} încercări!"
        
    return render_template_string(PAGINA_HTML, indiciu=indiciu)

@app.route("/reset")
def reset():
    if session.get('autentificat'):
        session['numar_secret'] = random.randint(1, 100)
        session['incercari'] = 0
    return render_template_string(PAGINA_HTML, indiciu="Jocul a fost resetat! Un nou număr a fost generat.")

@app.route("/logout")
def logout():
    session.clear()
    return index()

if __name__ == "__main__":
    app.run(debug=True)