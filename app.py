# app.py - Totul într-un singur fișier!
from flask import Flask, render_template_string, request, redirect, session, flash
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'cheie-secreta-pentru-sesiuni'

# Creăm folder pentru date dacă nu există
DATA_DIR = 'date_chestionare'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ============== HTML TEMPLATE-URI ==============

BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}CORE VET{% endblock %}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 20px; }
        h1 { color: #333; margin-bottom: 20px; font-size: 28px; }
        h2 { color: #667eea; margin: 20px 0 15px 0; font-size: 22px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
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
        
        .menu-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
        .menu-item { 
            background: #f8f9fa; padding: 20px; border-radius: 10px; 
            border-left: 4px solid #667eea; transition: all 0.3s;
        }
        .menu-item:hover { transform: translateX(5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        
        .question { background: #f8f9fa; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 3px solid #667eea; }
        .question p { font-weight: 600; margin-bottom: 10px; color: #444; }
        
        .scale { display: flex; gap: 10px; flex-wrap: wrap; }
        .scale label { 
            display: flex; flex-direction: column; align-items: center;
            padding: 10px 15px; border: 2px solid #ddd; border-radius: 8px;
            cursor: pointer; transition: all 0.3s;
        }
        .scale label:hover { border-color: #667eea; background: #f0f0ff; }
        .scale input { margin-bottom: 5px; }
        .scale small { font-size: 11px; color: #666; text-align: center; max-width: 80px; }
        
        .result-box { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;
        }
        .result-score { font-size: 42px; font-weight: bold; }
        
        .riasec-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0; }
        .riasec-item { background: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center; }
        .riasec-item.highlight { background: #667eea; color: white; transform: scale(1.05); }
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
        
        input[type="text"], input[type="password"], select, textarea {
            width: 100%; padding: 12px; border: 2px solid #ddd; 
            border-radius: 8px; font-size: 16px; margin: 5px 0 15px 0;
        }
        input:focus { outline: none; border-color: #667eea; }
        
        .nav { background: white; padding: 15px 30px; border-radius: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
        .nav a { color: #667eea; text-decoration: none; margin-left: 20px; font-weight: 500; }
        
        @media (max-width: 600px) {
            .riasec-grid { grid-template-columns: repeat(2, 1fr); }
            .scale label { padding: 8px 10px; }
        }
    </style>
</head>
<body>
    <div class="container">
        {% if session.user %}
        <div class="nav">
            <strong style="color: #667eea;">📊 CORE VET</strong>
            <div>
                <a href="/">Acasă</a>
                <a href="/logout">Logout ({{ session.user }})</a>
            </div>
        </div>
        {% endif %}
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for msg in messages %}
                    <div class="alert alert-red">{{ msg }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>
'''

# ============== CHESTIONARE ==============

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
            'titlu': 'B. VALORI PROFESIONALE (12 itemi)',
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
            'titlu': 'C. AUTOEFICACITATE (10 itemi)',
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
            'titlu': 'D. MANAGEMENTUL CARIEREI (14 itemi)',
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
            'titlu': 'E. ANGAJABILITATE (12 itemi)',
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
            'titlu': 'F. BARIERE ȘI SUPORT (10 itemi)',
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

# ============== FUNCȚII DE CALCUL ==============

def calculeaza_orientare(r):
    # RIASEC
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
    
    B = med([f'B{i}' for i in range(1,13)])
    C_ef = med([f'C{i}' for i in range(1,11)])
    D = med([f'D{i}' for i in range(1,15)])
    Ef = med([f'E{i}' for i in range(1,13)])
    F_sup = med(['F1','F2','F5','F7','F9'])
    F_bar = med(['F3','F4','F6','F8','F10'])
    
    return {
        'riasec': {'scoruri': scoruri, 'cod': cod, 'max': 15},
        'valori': {'scor': B, 'nivel': niv(B)},
        'autoeficacitate': {'scor': C_ef, 'nivel': niv(C_ef)},
        'management': {'scor': D, 'nivel': niv(D)},
        'angajabilitate': {'scor': Ef, 'nivel': niv(Ef)},
        'suport': {'scor': F_sup, 'nivel': niv(F_sup)},
        'bariere': {'scor': F_bar, 'nivel': niv(F_bar), 'alerta': F_bar>=4},
        'risc_abandon': int(r.get('F10',1))>=4
    }

def calculeaza_tranzitie(r):
    def med(l): return round(sum([int(r.get(x,3)) for x in l])/len(l), 2)
    def niv(s): return 'scăzut' if s<2.5 else 'mediu' if s<3.5 else 'ridicat'
    
    return {
        'plan': {'scor': med([f'T{i}' for i in range(1,6)]), 'nivel': niv(med([f'T{i}' for i in range(1,6)]))},
        'job_ready': {'scor': med([f'T{i}' for i in range(6,11)]), 'nivel': niv(med([f'T{i}' for i in range(6,11)]))},
        'study': {'scor': med([f'T{i}' for i in range(11,16)]), 'nivel': niv(med([f'T{i}' for i in range(11,16)]))},
        'mobility': {'scor': med([f'T{i}' for i in range(16,21)]), 'nivel': niv(med([f'T{i}' for i in range(16,21)]))},
        'support': {'scor': med([f'T{i}' for i in range(21,26)]), 'nivel': niv(med([f'T{i}' for i in range(21,26)]))},
 
