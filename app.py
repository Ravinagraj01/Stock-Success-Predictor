from flask import Flask, render_template, request

app = Flask(__name__)

# Signal map with (Signal, Success %)
signal_map = {
    "Resistance": ("Sell", 60),
    "Support": ("Buy", 60),
    "None": ("Hold", 0),
    "Green": ("Buy", 70),
    "Red": ("Sell", 70),
    "Above 60": ("Sell", 55),
    "B/w 40 – 60": ("Hold", 40),
    "Below 40": ("Buy", 55),
    "Red Vol Dec.": ("Buy", 50),
    "Blue Cross": ("Buy", 65),
    "Green Vol Dec.": ("Sell", 50),
    "Red Cross": ("Sell", 65),
    "Neutral": ("Hold",40)
}

@app.route('/', methods=['GET', 'POST'])
def index():
    final_signal = None
    final_success = None
    selections = {}

    if request.method == 'POST':
        buy_total = 0
        sell_total = 0
        hold_total = 0
        all_percentages = []
        deductions = 0
        deductions1 = 0

        for key in ['price_at', 'trend', 'rsi', 'macd']:
            val = request.form.get(key)
            if val in signal_map:
                signal, percent = signal_map[val]
                selections[key] = val
                all_percentages.append((signal, percent))

                if signal == "Buy":
                    buy_total += percent
                elif signal == "Sell":
                    sell_total += percent
                elif signal == "Hold":
                    hold_total += percent

        # Determine dominant signal based on total percentages
        dominant_signal = None
        if buy_total > sell_total:
            dominant_signal = "Buy"
        elif sell_total > buy_total:
            dominant_signal = "Sell"

        total = 0
        total1 = 0
        for signal, percent in all_percentages:
            if signal == "Hold":
                total1 += percent/2
                total += percent
            elif dominant_signal and signal != dominant_signal:
                deductions += percent
                deductions1 += percent
            else:
                total += percent
                total1 += percent
        sum = total + deductions
    
        final_success = round(max(((total1 - deductions1) / sum) * 100, 0), 2)

        final_signal = dominant_signal if dominant_signal else "Neutral"

    return render_template('index.html', signal=final_signal, success=final_success, selections=selections)

if __name__ == '__main__':
    app.run(debug=True)
