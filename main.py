from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Lista per memorizzare i round
rounds = []

@app.route('/')
def home():
    return render_template('home.html', rounds=rounds)

@app.route('/new-round', methods=['GET', 'POST'])
def new_round():
    if request.method == 'POST':
        num_holes = request.form['num_holes']
        start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Registra la data e l'ora del round
        current_round = {
            'num_holes': num_holes,
            'start_date': start_date,  # Aggiungi la data del round
            'holes': []  # Inizializza la lista delle buche
        }
        rounds.append(current_round)
        return redirect(url_for('add_hole', round_index=len(rounds) - 1))
    return render_template('new_round.html')

@app.route('/add-holes/<int:round_index>', methods=['GET', 'POST'])
def add_hole(round_index):
    if request.method == 'POST':
        hole_number = request.form['hole_number']
        fairway_hit = request.form['fairway_hit'] or 0  # Imposta 0 di default
        green_in_regulation = request.form['green_in_regulation'] or 0  # Imposta 0 di default
        putts = request.form['putts']
        penalties = request.form['penalties']
        par = request.form['par']
        strokes = request.form['strokes']

        # Salviamo le statistiche in un dizionario
        hole_stats = {
            'hole_number': hole_number,
            'fairway_hit': min(int(fairway_hit), 1),  # Imposta max 1
            'green_in_regulation': min(int(green_in_regulation), 1),  # Imposta max 1
            'putts': putts,
            'penalties': penalties,
            'par': par,
            'strokes': strokes
        }

        # Aggiungi le statistiche alla lista della buca del round specifico
        rounds[round_index]['holes'].append(hole_stats)

        # Controlla se è l'ultimo buca del round
        if len(rounds[round_index]['holes']) < int(rounds[round_index]['num_holes']):
            return redirect(url_for('add_hole', round_index=round_index))
        else:
            return redirect(url_for('home'))

    # Mostra la maschera per aggiungere le statistiche della buca
    return render_template('add_hole.html', round_index=round_index, current_round=rounds[round_index])

@app.route('/stats')
def stats():
    return render_template('stats.html', rounds=rounds)

@app.route('/goals')
def goals():
    return render_template('goals.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
