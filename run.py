from app import app, db
from app.models import Sofor, Alarm, SesLog, VardiyaSesKaydi, YolcuYorum, AracKonum

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Sofor': Sofor,
        'Alarm': Alarm,
        'SesLog': SesLog,
        'VardiyaSesKaydi': VardiyaSesKaydi,
        'YolcuYorum': YolcuYorum,
        'AracKonum': AracKonum
    }

if __name__ == '__main__':
    print("Surus Guvenlik Web Sunucusu Baslatiliyor...")
    app.run(host='0.0.0.0', port=5000, debug=True)
