from app import create_app, db
from app.models import Sofor, Alarm, SesLog, VardiyaSesKaydi, YolcuYorum, AracKonum

app = create_app()

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
    print("Moduler Mobil API Sunucusu Baslatiliyor...")
    print("Cihazlardan (Flutter) baglanmak icin 'http://0.0.0.0:5000' kullanabilirsiniz.")
    app.run(host='0.0.0.0', port=5000, debug=True)


