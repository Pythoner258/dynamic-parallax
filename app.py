
from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            # Načtení dat z formuláře
            T_m = float(request.form['T_m'])
            a = float(request.form['a'])
            b = float(request.form['b'])
            m1 = float(request.form['m1'])
            m2 = float(request.form['m2'])
            M1 = float(request.form['M1'])
            M2 = float(request.form['M2'])
            presnost = float(request.form['presnost'])

            # Konstanty
            L_S = 3.828e26
            M_S = 4.83

            # Výpočet oběžné periody
            h = (a**2 - b**2)**0.5
            epsilon = a * b * (math.acos(h / a) - h / a**2 * ((a**2 - h**2)**0.5))
            S = math.pi * a * b
            T = S / epsilon * T_m

            # Iterace
            M_predchozi = M1 + M2
            while True:
                a_i = ((M1 + M2) * T**2)**(1/3)
                d = a_i / a
                mag1 = m1 + 5 - 5 * math.log10(d)
                mag2 = m2 + 5 - 5 * math.log10(d)
                L1 = L_S * 10 ** ((M_S - mag1) / 2.5)
                L2 = L_S * 10 ** ((M_S - mag2) / 2.5)
                M1_nove = (L1 / L_S) ** (2/7)
                M2_nove = (L2 / L_S) ** (2/7)
                M_nove = M1_nove + M2_nove
                rozdil = abs((M_nove - M_predchozi) / M_predchozi * 100)
                if rozdil < presnost:
                    break
                M1, M2 = M1_nove, M2_nove
                M_predchozi = M_nove

            # Výsledek jako string
            result = (
                f"Oběžná perioda T: {T:.2f} roků\n"
                f"Velká poloosa a: {a_i:.2f} AU\n"
                f"Vzdálenost soustavy d: {d:.2f} pc\n"
                f"Absolutní magnituda primární složky M1: {mag1:.2f}\n"
                f"Absolutní magnituda sekundární složky M2: {mag2:.2f}\n"
                f"Zářivý výkon primární složky L1: {L1:.2e} W\n"
                f"Zářivý výkon sekundární složky L2: {L2:.2e} W\n"
                f"Hmotnost primární složky M1: {M1:.2f} M☉\n"
                f"Hmotnost sekundární složky M2: {M2:.2f} M☉\n"
                f"Přesnost výpočtu: {rozdil:.2f} %"
            )

        except Exception as e:
            result = f"Chyba při výpočtu: {e}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)



