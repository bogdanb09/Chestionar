# app.py - Part 1/3 - Imports and CSS
from flask import Flask, request, redirect, session, flash
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'cheie-secreta-pentru-sesiuni-2024'

# CSS styles
CSS = '''
<style>
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
.container { max-width: 900px; margin: 0 auto; }
.card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 20px; }
h1 { color: #333; margin-bottom: 20px; font-size: 28px; }
h2 { color: #667eea; margin: 20px 0 15px 0; font-size: 22px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
h3 { color: #444; margin: 15px 0; font-size: 18px; }
.btn { 
    display: inline-block; padding: 12px 25px; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; text-decoration: none; border-radius: 25px; 
    border: none; cursor: pointer; font-size: 16px; margin: 5px;
    transition: transform 0.2s;
}
.btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102,126,234,0.4); }
.btn-green { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
.btn-red { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); }
.btn-orange { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.btn-blue { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.btn-gray { background: #6c757d; }

.menu-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
.menu-item { background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea; }
.menu-item:hover { transform: translateX(5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }

.question { background: #f8f9fa; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 3px solid #667eea; }
.question p { font-weight: 600; margin-bottom: 10px; color: #444; }

.scale { display: flex; gap: 10px; flex-wrap: wrap; }
.scale label { 
    display: flex; flex-direction: column; align-items: center;
    padding: 10px 15px; border: 2px solid #ddd; border-radius: 8px;
    cursor: pointer; transition: all 0.3s; background: white;
}
.scale label:hover { border-color: #667eea; background: #f0f0ff; }
.scale input { margin-bottom: 5px; }
.scale small { font-size: 11px; color: #666; text-align: center; max-width: 80px; }

.riasec-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0; }
.riasec-item { background: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid transparent; }
.riasec-item.highlight { background: #667eea; color: white; transform: scale(1.05); border-color: #764ba2; }
.riasec-letter { font-size: 28px; font-weight: bold; color: #667eea; }
.riasec-item.highlight .riasec-letter { color: white; }

.alert { padding: 15px; border-radius: 8px; margin: 15px 0; }
.alert-red { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.alert-green { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.alert-yellow { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }

.progress-bar { width: 100%; height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden; margin: 10px 0; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); }

.score-low { color: #dc3545; }
.score-med { color: #ffc107; }
.score-high { color: #28a745; }

input[type="text"] { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; margin: 5px 0 15px 0; }
input:focus { outline: none; border-color: #667eea; }

.nav { background: white; padding: 15px 30px; border-radius: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
.nav a { color: #667eea; text-decoration: none; margin-left: 20px; font-weight: 500; }
.nav a:hover { text-decoration: underline; }

table { width: 100%; border-collapse: collapse; margin: 20px 0; }
th { background: #667eea; color: white; padding: 12px; text-align: left; }
td { padding: 12px; border-bottom: 1px solid #ddd; }
tr:hover { background: #f5f5f5; }

.center { text-align: center; }
.mt-20 { margin-top: 20px; }
.mb-20 { margin-bottom: 20px; }

@media (max-width: 600px) {
    .riasec-grid { grid-template-columns: repeat(2, 1fr); }
    .scale label { padding: 8px 10px; }
    .nav { flex-direction: column; gap: 10px; }
    .nav div { margin-top: 10px; }
}
</style>
'''
# Part 2/3 - Questionnaires

# Create data directory
DATA_DIR = 'date_chestionare'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Chestionar 1: Orientare
CHESTIONAR_ORIENTARE = {
    'titlu': '🎯 Chestionar de Orientare în Carieră (CORE VET)',
    'sectiuni': {
        'A': {
            'titlu': 'A. INTERESE PROFESIONALE (RIASEC)',
            'intrebari': {
                'A1': 'Îmi place să lucrez cu unelte, aparate sau mașini.',
                'A2': 'Prefer activități practice, unde văd rezultatul imediat.',
                'A3': 'Mă simt bine când repar, montez sau construiesc ceva.',
                'A4': 'Îmi place să caut cauza unei probleme și să o rezolv pas cu pas.',
                'A5': 'Mă atrag sarcinile unde trebuie să măsor, testez sau verific.',
                'A6': 'Îmi place să învăț cum funcționează lucrurile, în detaliu.',
                'A7': 'Îmi place să creez sau să îmbunătățesc aspectul unui produs.',
                'A8': 'Îmi place să găsesc soluții originale.',
                'A9': 'Mă atrag activitățile unde contează designul sau estetica.',
                'A10': 'Îmi place să ajut oamenii să rezolve probleme.',
                'A11': 'Mă simt bine când lucrez cu oameni.',
                'A12': 'Îmi place să explic sau să îndrum pe alții.',
                'A13': 'Îmi place să iau inițiativa.',
                'A14': 'Îmi place să conving sau să negociez.',
                'A15': 'Mă văd coordonând un mic proiect sau echipă.',
                'A16': 'Îmi place să lucrez organizat, cu reguli clare.',
                'A17': 'Mă descurc bine cu evidențe și documente.',
                'A18': 'Prefer sarcini clare și bine structurate.',
            }
        },
        'B': {
            'titlu': 'B. VALORI PROFESIONALE',
            'intrebari': {
                'B1': 'Contează să am un venit stabil.',
                'B2': 'Îmi doresc o meserie sigură.',
                'B3': 'Munca mea trebuie să fie utilă altora.',
                'B4': 'Vreau posibilități de creștere profesională.',
                'B5': 'Îmi doresc un colectiv respectuos.',
                'B6': 'Prefer un program de lucru clar.',
                'B7': 'Vreau să am autonomie la muncă.',
                'B8': 'Îmi doresc apreciere pentru munca mea.',
                'B9': 'Contează condițiile de muncă sigure.',
                'B10': 'Vreau să învăț lucruri noi.',
                'B11': 'Îmi doresc echilibru muncă-viață.',
                'B12': 'Prefer să lucrez aproape de casă.',
            }
        },
        'C': {
            'titlu': 'C. AUTOEFICACITATE',
            'intrebari': {
                'C1': 'Pot atinge obiective profesionale dacă muncesc.',
                'C2': 'Pot învăța abilități noi.',
                'C3': 'Învăț din greșeli.',
                'C4': 'Pot cere ajutor când nu înțeleg.',
                'C5': 'Pot lucra sub presiune.',
                'C6': 'Îmi organizez timpul bine.',
                'C7': 'Pot comunica cu mentorul.',
                'C8': 'Mă adaptez la reguli noi.',
                'C9': 'Accept feedback.',
                'C10': 'Cred că pot obține un loc de muncă.',
            }
        },
        'D': {
            'titlu': 'D. MANAGEMENTUL CARIEREI',
            'intrebari': {
                'D1': 'Știu ce opțiuni am după absolvire.',
                'D2': 'Am un plan pentru viitor.',
                'D3': 'Pot compara meserii diferite.',
                'D4': 'Mă informez despre piața muncii.',
                'D5': 'Știu unde să caut informații despre joburi.',
                'D6': 'Îmi stabilesc obiective clare.',
                'D7': 'Am plan de rezervă.',
                'D8': 'Cunosc ce cer angajatorii.',
                'D9': 'Știu ce trebuie să mai învăț.',
                'D10': 'Pot lua decizii.',
                'D11': 'Folosesc practica pentru a testa meseria.',
                'D12': 'Pot cere sprijin profesional.',
                'D13': 'Îmi urmăresc progresul.',
                'D14': 'Înțeleg ce înseamnă calificarea mea.',
            }
        },
        'E': {
            'titlu': 'E. ANGAJABILITATE',
            'intrebari': {
                'E1': 'Pot spune clar ce știu să fac.',
                'E2': 'Pot face un CV.',
                'E3': 'Am un portofoliu.',
                'E4': 'Știu unde să caut joburi.',
                'E5': 'Pot scrie un mesaj unui angajator.',
                'E6': 'Pot răspunde la interviu.',
                'E7': 'Știu ce întrebări să pun la interviu.',
                'E8': 'Îmi cunosc drepturile ca angajat.',
                'E9': 'Mă prezint profesionist.',
                'E10': 'Respect programul.',
                'E11': 'Pot cere recomandări.',
                'E12': 'Accept feedback profesional.',
            }
        },
        'F': {
            'titlu': 'F. BARIERE ȘI SUPORT',
            'intrebari': {
                'F1': 'Familia mă sprijină.',
                'F2': 'Am o persoană care mă ghidează.',
                'F3': 'Lipsa banilor mă împiedică.',
                'F4': 'Transportul este o problemă.',
                'F5': 'Am acces la informații.',
                'F6': 'Mi-e frică că nu voi găsi job.',
                'F7': 'Sunt dispus(ă) să merg în alt oraș.',
                'F8': 'Nu am relații utile.',
                'F9': 'Știu la cine să apelez în școală.',
                'F10': 'M-am gândit să renunț la studii.',
            }
        }
    }
}
# Part 3/3 - Routes and Main

# Chestionar 2: Tranziție
CHESTIONAR_TRANZITIE = {
    'titlu': '📋 Tranziție după Absolvire',
    'sectiuni': {
        'T': {
            'titlu': 'Evaluare pregătire tranziție',
            'intrebari': {f'T{i}': [
                'Știu clar ce voi face în primele 3 luni după absolvire.',
                'Am un Plan A (varianta principală).',
                'Am și un Plan B.',
                'Știu ce pași concreți trebuie să fac.',
                'Am discutat planul cu un adult/specialist.',
                'Am un CV sau știu să-l fac rapid.',
                'Știu unde să caut oferte de muncă.',
                'Știu cui pot cere recomandare.',
                'Mă simt pregătit(ă) pentru interviu.',
                'Știu să mă prezint profesionist.',
                'Cunosc opțiunile de studii după absolvire.',
                'Vreau să-mi cresc calificarea.',
                'Știu ce competențe îmi lipsesc.',
                'Pot combina munca cu învățarea.',
                'Am identificat un curs/școală.',
                'Sunt dispus(ă) să lucrez în alt oraș.',
                'Sunt dispus(ă) să lucrez peste hotare.',
                'Cunosc riscurile muncii neoficiale.',
                'Știu ce documente sunt importante.',
                'Pot lua decizii informate despre migrație.',
                'Am sprijin din partea familiei.',
                'Am un mentor.',
                'Am acces la resurse.',
                'Știu unde să cer ajutor.',
                'Am oportunități reale.',
                'Mă îngrijorează că nu voi găsi job.',
                'Mă tem că nu sunt suficient de bun.',
                'Problemele financiare pot bloca planul.',
                'Transportul ar putea fi o problemă.',
                'Amân pașii importanți.'
            ][i-1] for i in range(1, 31)}
        }
    }
}

# Chestionar 3: Abandon
CHESTIONAR_ABANDON = {
    'titlu': '⚠️ Risc de Abandon Școlar',
    'sectiuni': {
        'R': {
            'titlu': 'Factori de risc și protecție',
            'intrebari': {f'R{i}': [
                'Mă simt motivat(ă) să continui studiile.',
                'Îmi place specialitatea pe care o studiez.',
                'Înțeleg legătura dintre școală și viitorul meu profesional.',
                'Mă simt sprijinit(ă) de profesori.',
                'Mă simt acceptat(ă) în colectiv.',
                'Absențele mele au crescut în ultima perioadă.',
                'Mi se pare prea greu ce se cere la școală.',
                'Problemele financiare îmi afectează frecvența la școală.',
                'Drumul/transportul până la școală este dificil.',
                'Am dificultăți de concentrare la lecții.',
                'Mă gândesc uneori să renunț la școală.',
                'Familia mă încurajează să continui studiile.',
                'Am un adult în școală cu care pot vorbi deschis.',
                'Mă simt obosit(ă) sau lipsit(ă) de energie pentru școală.',
                'Cred că pot termina cu succes studiile.',
                'Mă simt stresat(ă) din cauza cerințelor școlare.',
                'Am colegi care mă susțin.',
                'Lipsa banilor pentru rechizite/transport este o problemă.',
                'Simt că nu fac față evaluărilor.',
                'Consider că ar fi mai bine să mă angajez decât să continui școala.'
            ][i-1] for i in range(1, 21)}
        }
    }
}

# Chestionar 4: Practică
CHESTIONAR_PRACTICA = {
    'titlu': '💼 Practică Profesională și Job Shadowing',
    'sectiuni': {
        'P': {
            'titlu': 'Evaluarea experienței de practică',
            'intrebari': {f'P{i}': [
                'Practica m-a ajutat să înțeleg mai bine meseria mea.',
                'Sarcinile primite la practică au fost clare.',
                'Am avut ce învăța din activitățile de la practică.',
                'Mentorul/maistrul mi-a explicat ce aveam de făcut.',
                'Am primit feedback despre munca mea.',
                'M-am simțit respectat(ă) la locul de practică.',
                'Condițiile de muncă au fost sigure.',
                'Practica a fost legată de specialitatea mea.',
                'Mi-a plăcut mediul de lucru.',
                'Aș dori să lucrez în acest domeniu după absolvire.',
                'Activitatea de job shadowing m-a ajutat să cunosc meseria.',
                'Observarea unui profesionist m-a ajutat să decid mai bine.',
                'Am înțeles ce presupune o zi de muncă.',
                'Am putut pune întrebări despre meserie.',
                'Experiența de job shadowing a fost utilă.',
                'Programul de practică a fost bine organizat.',
                'Comunicarea cu mentorul a fost bună.',
                'M-am integrat bine în echipă.',
                'Mi-a crescut încrederea în mine.',
                'Practica m-a motivat să continui studiile.'
            ][i-1] for i in range(1, 21)}
        }
    }
}

# Chestionar 5: Competențe
CHESTIONAR_COMPETENTE = {
    'titlu': '🤝 Competențe Interpersonale pentru Angajabilitate',
    'sectiuni': {
        'S': {
            'titlu': 'Evaluare competențe soft',
            'intrebari': {f'S{i}': [
                'Pot comunica clar cu colegii și superiorii.',
                'Ascult cu atenție când cineva îmi explică ceva.',
                'Pot lucra bine în echipă.',
                'Îmi respect responsabilitățile.',
                'Ajung la timp la activități.',
                'Pot gestiona conflicte fără ceartă.',
                'Accept feedback fără să mă supăr.',
                'Îmi organizez bine timpul.',
                'Pot rezolva probleme simple singur(ă).',
                'Mă adaptez la schimbări.',
                'Pot lucra sub presiune.',
                'Sunt politicos/politicoasă cu ceilalți.',
                'Pot cere ajutor când am nevoie.',
                'Îmi controlez emoțiile la muncă.',
                'Îmi asum greșelile.',
                'Îmi finalizez sarcinile începute.',
                'Pot urma instrucțiuni.',
                'Îmi place să colaborez cu alții.',
                'Sunt deschis(ă) să învăț lucruri noi.',
                'Mă comport profesionist.'
            ][i-1] for i in range(1, 21)}
        }
    }
}

# Calculation functions
def calc_orientare(r):
    R = sum([int(r.get(f'A{i}',3)) for i in range(1,4)])
    I = sum([int(r.get(f'A{i}',3)) for i in range(4,7)])
    A = sum([int(r.get(f'A{i}',3)) for i in range(7,10)])
    S = sum([int(r.get(f'A{i}',3)) for i in range(10,13)])
    E = sum([int(r.get(f'A{i}',3)) for i in range(13,16)])
    C = sum([int(r.get(f'A{i}',3)) for i in range(16,19)])
    
    scoruri = {'R':R, 'I':I, 'A':A, 'S':S, 'E':E, 'C':C}
    sortate = sorted(scoruri.items(), key=lambda x:x[1], reverse=True)
    cod = f"{sortate[0][0]}-{sortate[1][0]}"
    
    def med(l): return round(sum([int(r.get(x,3)) for x in l])/len(l), 2)
    def niv(s): return 'scăzut' if s<2.5 else 'mediu' if s<3.5 else 'ridicat'
    
    return {
        'riasec': {'scoruri': scoruri, 'cod': cod, 'max': 15},
        'valori': {'scor': med([f'B{i}' for i in range(1,13)]), 'nivel': niv(med([f'B{i}' for i in range(1,13)]))},
        'autoeficacitate': {'scor': med([f'C{i}' for i in range(1,11)]), 'nivel': niv(med([f'C{i}' for i in range(1,11)]))},
        'management': {'scor': med([f'D{i}' for i in range(1,15)]), 'nivel': niv(med([f'D{i}' for i in range(1,15)]))},
        'angajabilitate': {'scor': med([f'E{i}' for i in range(1,13)]), 'nivel': niv(med([f'E{i}' for i in range(1,13)]))},
        'suport': {'scor': med(['F1','F2','F5','F7','F9']), 'nivel': niv(med(['F1','F2','F5','F7','F9']))},
        'bariere': {'scor': med(['F3','F4','F6','F8','F10']), 'nivel': niv(med(['F3','F4','F6','F8','F10'])), 'alerta': med(['F3','F4','F6','F8','F10'])>=4},
        'risc_abandon': int(r.get('F10',1))>=4
    }

def calc_tranzitie(r):
    def med(l): return round(sum([int(r.get(x,3)) for x in l])/len(l), 2)
    def niv(s): return 'scăzut' if s<2.5 else 'mediu' if s<3.5 else 'ridicat'
    return {
        'plan': {'scor': med([f'T{i}' for i in range(1,6)]), 'nivel': niv(med([f'T{i}' for i in range(1,6)]))},
        'job_ready': {'scor': med([f'T{i}' for i in range(6,11)]), 'nivel': niv(med([f'T{i}' for i in range(6,11)]))},
        'study': {'scor': med([f'T{i}' for i in range(11,16)]), 'nivel': niv(med([f'T{i}' for i in range(11,16)]))},
        'mobility': {'scor': med([f'T{i}' for i in range(16,21)]), 'nivel': niv(med([f'T{i}' for i in range(16,21)]))},
        'support': {'scor': med([f'T{i}' for i in range(21,26)]), 'nivel': niv(med([f'T{i}' for i in range(21,26)]))},
        'barriers': {'scor': med([f'T{i}' for i in range(26,31)]), 'nivel': niv(med([f'T{i}' for i in range(26,31)]))}
    }

def calc_abandon(r):
    def med(l): return round(sum([int(r.get(f'R{i}',3)) for i in l])/len(l), 2)
    def niv_risc(s): return 'ridicat' if s>3.5 else 'mediu' if s>2.5 else 'scăzut'
    
    motiv = med([1,2,3,15])
    sup = med([4,5,12,13,17])
    dif = med([6,7,10,14,16,19])
    bar = med([8,9,18])
    intent = med([11,20])
    
    risc_gen = (6-motiv + 6-sup + dif + bar + intent*2)/5
    
    return {
        'motivatie': {'scor': motiv, 'nivel': niv_risc(6-motiv)},
        'suport': {'scor': sup, 'nivel': niv_risc(6-sup)},
        'dificultati': {'scor': dif, 'nivel': niv_risc(dif)},
        'bariere': {'scor': bar, 'nivel': niv_risc(bar)},
        'intentie': {'scor': intent, 'nivel': niv_risc(intent)},
        'risc_general': round(risc_gen, 2),
        'alerta': intent>=4 or motiv<2
    }

def calc_practica(r):
    def med(l): return round(sum([int(r.get(f'P{i}',3)) for i in l])/len(l), 2)
    def niv(s): return 'scăzut' if s<2.5 else 'mediu' if s<3.5 else 'ridicat'
    return {
        'utilitate': {'scor': med([1,3,8,10,20]), 'nivel': niv(med([1,3,8,10,20]))},
        'mentorat': {'scor': med([4,5,14,17]), 'nivel': niv(med([4,5,14,17]))},
        'mediu': {'scor': med([6,7,9,18]), 'nivel': niv(med([6,7,9,18]))},
        'shadowing': {'scor': med([11,12,13,15]), 'nivel': niv(med([11,12,13,15]))},
        'organizare': {'scor': med([2,16]), 'nivel': niv(med([2,16]))}
    }

def calc_competente(r):
    def med(l): return round(sum([int(r.get(f'S{i}',3)) for i in l])/len(l), 2)
    def niv(s): return 'scăzut' if s<2.5 else 'mediu' if s<3.5 else 'ridicat'
    return {
        'comunicare': {'scor': med([1,2,7,12]), 'nivel': niv(med([1,2,7,12]))},
        'echipa': {'scor': med([3,18]), 'nivel': niv(med([3,18]))},
        'responsabilitate': {'scor': med([4,5,15,16]), 'nivel': niv(med([4,5,15,16]))},
        'adaptabilitate': {'scor': med([9,10,11,19]), 'nivel': niv(med([9,10,11,19]))},
        'autocontrol': {'scor': med([6,13,14,17]), 'nivel': niv(med([6,13,14,17]))},
        'profesionalism': {'scor': med([8,20]), 'nivel': niv(med([8,20]))}
    }

# HTML helper
def render_page(title, content, nav=True):
    nav_html = ''
    if nav and session.get('user'):
        nav_html = f'''
        <div class="nav">
            <strong style="color: #667eea;">📊 CORE VET</strong>
            <div>
                <a href="/">Acasă</a>
                <a href="/rezultate">Rezultate</a>
                <a href="/logout">Logout ({session["user"]})</a>
            </div>
        </div>
        '''
    return f'''<!DOCTYPE html>
<html lang="ro"><head><meta charset="UTF-8"><title>{title}</title>{CSS}</head>
<body><div class="container">{nav_html}{content}</div></body></html>'''

# Routes
@app.route('/')
def home():
    if not session.get('user'):
        return redirect('/login')
    content = f'''
    <div class="card center"><h1>Bun venit, {session["user"]}! 👋</h1>
    <p style="color: #666; margin: 15px 0;">Alege un chestionar:</p></div>
    <div class="menu-grid">
        <div class="menu-item"><h3>🎯 Orientare în Carieră</h3><p style="font-size: 14px; color: #666;">Profil RIASEC, valori, autoeficacitate</p><a href="/chestionar/orientare" class="btn">Completează</a></div>
        <div class="menu-item" style="border-left-color: #11998e;"><h3>📋 Tranziție după Absolvire</h3><p style="font-size: 14px; color: #666;">Pregătire pentru piața muncii</p><a href="/chestionar/tranzitie" class="btn btn-green">Completează</a></div>
        <div class="menu-item" style="border-left-color: #eb3349;"><h3>⚠️ Risc de Abandon</h3><p style="font-size: 14px; color: #666;">Identificare factori de risc</p><a href="/chestionar/abandon" class="btn btn-red">Completează</a></div>
        <div class="menu-item" style="border-left-color: #f093fb;"><h3>💼 Practică Profesională</h3><p style="font-size: 14px; color: #666;">Evaluare experiență practică</p><a href="/chestionar/practica" class="btn btn-orange">Completează</a></div>
        <div class="menu-item" style="border-left-color: #4facfe;"><h3>🤝 Competențe Interpersonale</h3><p style="font-size: 14px; color: #666;">Abilități pentru angajare</p><a href="/chestionar/competente" class="btn btn-blue">Completează</a></div>
    </div>'''
    return render_page('Dashboard', content)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        session['user'] = user
        user_dir = os.path.join(DATA_DIR, user)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        return redirect('/')
    content = '''
    <div class="card center" style="max-width: 400px; margin: 0 auto;"><h1>🔐 Intrare</h1>
    <form method="POST"><input type="text" name="user" placeholder="Numele tău" required autofocus style="margin: 20px 0;">
    <button type="submit" class="btn" style="width: 100%;">Intră în platformă</button></form>
    <p style="margin-top: 20px; color: #666; font-size: 14px;">Doar introdu numele pentru a începe.</p></div>'''
    return render_page('Login', content, nav=False)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/chestionar/<tip>', methods=['GET','POST'])
def chestionar(tip):
    if not session.get('user'):
        return redirect('/login')
    chestionare = {'orientare': CHESTIONAR_ORIENTARE, 'tranzitie': CHESTIONAR_TRANZITIE, 
                   'abandon': CHESTIONAR_ABANDON, 'practica': CHESTIONAR_PRACTICA, 'competente': CHESTIONAR_COMPETENTE}
    if tip not in chestionare:
        return redirect('/')
    c = chestionare[tip]
    if request.method == 'POST':
        raspunsuri = request.form.to_dict()
        rezultate = {'orientare': calc_orientare, 'tranzitie': calc_tranzitie, 
                     'abandon': calc_abandon, 'practica': calc_practica, 'competente': calc_competente}[tip](raspunsuri)
        data = {'tip': tip, 'data': datetime.now().isoformat(), 'raspunsuri': raspunsuri, 'rezultate': rezultate}
        filename = f"{tip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(DATA_DIR, session['user'], filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return redirect(f'/rezultat/{tip}/{filename}')
    
    intrebari_html = ''
    for cod_sect, sectiune in c['sectiuni'].items():
        intrebari_html += f'<h2>{sectiune["titlu"]}</h2>'
        for cod, text in sectiune['intrebari'].items():
            intrebari_html += f'''<div class="question"><p>{cod}. {text}</p><div class="scale">
                <label><input type="radio" name="{cod}" value="1" required><span>1</span><small>Deloc</small></label>
                <label><input type="radio" name="{cod}" value="2"><span>2</span><small>Mai degrabă nu</small></label>
                <label><input type="radio" name="{cod}" value="3"><span>3</span><small>Parțial</small></label>
                <label><input type="radio" name="{cod}" value="4"><span>4</span><small>Mai degrabă da</small></label>
                <label><input type="radio" name="{cod}" value="5"><span>5</span><small>Foarte</small></label>
            </div></div>'''
    
    content = f'''<div class="card"><h1>{c['titlu']}</h1><form method="POST" id="form">{intrebari_html}
    <div class="center mt-20"><button type="submit" class="btn" style="font-size: 18px; padding: 15px 40px;">Vezi rezultatele</button>
    <a href="/" class="btn btn-gray">Anulează</a></div></form></div>
    <script>document.getElementById('form').addEventListener('submit', function(e) {{
        const all = document.querySelectorAll('.question'); let ok = true;
        all.forEach(q => {{ if (!q.querySelector('input:checked')) ok = false; }});
        if (!ok) {{ e.preventDefault(); alert('Răspunde la toate întrebările!'); }}
    }});</script>'''
    return render_page(c['titlu'], content)

@app.route('/rezultat/<tip>/<filename>')
def rezultat(tip, filename):
    if not session.get('user'):
        return redirect('/login')
    filepath = os.path.join(DATA_DIR, session['user'], filename)
    if not os.path.exists(filepath):
        return redirect('/')
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    r = data['rezultate']
    
    if tip == 'orientare':
        riasec_items = ''.join([f'<div class="riasec-item {"highlight" if lit in r["riasec"]["cod"] else ""}"><div class="riasec-letter">{lit}</div><div style="font-size: 24px; font-weight: bold;">{scor}</div><small>/15</small></div>' for lit, scor in r['riasec']['scoruri'].items()])
        content = f'''<h2>Profilul tău RIASEC: <span style="color: #667eea;">{r['riasec']['cod']}</span></h2>
        <div class="riasec-grid">{riasec_items}</div>
        <div class="menu-grid">
            <div class="card center"><h4>Valori</h4><div class="result-score score-{r['valori']['nivel']}">{r['valori']['scor']}</div><div class="score-{r['valori']['nivel']}">{r['valori']['nivel']}</div></div>
            <div class="card center"><h4>Autoeficacitate</h4><div class="result-score score-{r['autoeficacitate']['nivel']}">{r['autoeficacitate']['scor']}</div><div class="score-{r['autoeficacitate']['nivel']}">{r['autoeficacitate']['nivel']}</div></div>
            <div class="card center"><h4>Management</h4><div class="result-score score-{r['management']['nivel']}">{r['management']['scor']}</div><div class="score-{r['management']['nivel']}">{r['management']['nivel']}</div></div>
            <div class="card center"><h4>Angajabilitate</h4><div class="result-score score-{r['angajabilitate']['nivel']}">{r['angajabilitate']['scor']}</div><div class="score-{r['angajabilitate']['nivel']}">{r['angajabilitate']['nivel']}</div></div>
        </div>
        <div class="menu-grid">
            <div class="card" style="border-left: 4px solid #28a745;"><h4>Suport</h4><div style="font-size: 36px; color: #28a745;">{r['suport']['scor']}</div><div>{r['suport']['nivel']}</div></div>
            <div class="card" style="border-left: 4px solid #dc3545;"><h4>Bariere</h4><div style="font-size: 36px; color: #dc3545;">{r['bariere']['scor']}</div><div>{r['bariere']['nivel']}</div>{'<p style="color: #dc3545;"><strong>⚠️ Bariere semnificative!</strong></p>' if r['bariere']['alerta'] else ''}</div>
        </div>{'<div class="alert alert-red"><strong>🚨 Alertă:</strong> Intenție de abandon!</div>' if r['risc_abandon'] else ''}'''
    
    elif tip == 'tranzitie':
        labels = {'plan': '📋 Planificare', 'job_ready': '💼 Job Ready', 'study': '📚 Studii', 'mobility': '🌍 Mobilitate', 'support': '🤝 Suport', 'barriers': '⚠️ Bariere'}
        items = ''.join([f'<div class="card center"><h4>{labels.get(k,k)}</h4><div style="font-size: 42px; font-weight: bold; color: {"#dc3545" if v["nivel"]=="scăzut" else "#ffc107" if v["nivel"]=="mediu" else "#28a745"}">{v["scor"]}</div><div>{v["nivel"]}</div></div>' for k,v in r.items()])
        content = f'<h2>Pregătirea pentru tranziție</h2><div class="menu-grid">{items}</div>'
    
    elif tip == 'abandon':
        bg = '#d4edda' if r['risc_general'] < 2.5 else '#fff3cd' if r['risc_general'] < 3.5 
