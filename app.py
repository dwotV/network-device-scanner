from scanner.scan import scan
from datetime import datetime
from scanner.network import network
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'
db = SQLAlchemy(app)

class Device(db.Model):
    mac = db.Column(db.String(17), primary_key=True)
    ip = db.Column(db.String(15), nullable=False)
    description = db.Column(db.String(100), default='Unknown device')
    vendor = db.Column(db.String(60))
    status = db.Column(db.String(10), default = 'New Device')
    registered = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def run_scan():
    ip_range = network()[1]
    discovered_devices = scan(ip_range)
    scanned_macs = set()

    for device in discovered_devices:
        mac = device['mac'].upper()
        scanned_macs.add(mac)

        device_db = Device.query.filter_by(mac=mac).first()

        if device_db:
            device_db.ip = device['ip']
            device_db.status = 'Online'
            device_db.last_seen = datetime.utcnow()
        else:
            db.session.add(Device(
                mac=mac,
                ip=device['ip'],
                vendor=device['vendor'],
                status='Online'
            ))

    if scanned_macs:
        Device.query.filter(
            ~Device.mac.in_(scanned_macs)
        ).update(
            {Device.status: 'Offline'},
            synchronize_session=False
        )

    db.session.commit()

@app.route('/')
def index():
    ip_range = network()[1]

    filter_by = request.args.get('filter')

    query = Device.query

    if filter_by == 'online':
        query = query.filter_by(status='Online')
    elif filter_by == 'offline':
        query = query.filter_by(status='Offline')
    elif filter_by == 'unknown':
        query = query.filter_by(registered=False)
    elif filter_by == 'blocked':
        query = query.filter_by(status='Blocked')

    devices = query.all()

    total_devices = Device.query.count()
    online_devices = Device.query.filter_by(status='Online').count()
    offline_devices = Device.query.filter_by(status='Offline').count()
    blocked_devices = Device.query.filter_by(status='Blocked').count()
    total_unknown = Device.query.filter_by(registered=False).count()
    #devices = Device.query.all() 

    return render_template(
        'index.html',
        devices = devices,
        network = ip_range,
        total_devices = total_devices,
        total_unknown = total_unknown,
        online_devices = online_devices,
        offline_devices = offline_devices,
        blocked_devices = blocked_devices
    )

@app.route('/scan', methods=['POST'])
def scan_network():
    run_scan()
    return redirect(url_for('index'))

@app.route('/whitelist')
def whitelist():
    registered_devices = Device.query.filter_by(registered=True).all()
    total_known = Device.query.filter_by(registered=True).count()
    return render_template('whitelist.html', devices=registered_devices, total_known = total_known)

@app.route('/add', methods=['POST'])
def add_device():
    mac = request.form.get('mac').upper()
    desc = request.form.get('description')

    try:
        device = Device.query.get_or_404(mac)

        if device:
            device.description = desc
            device.registered = True
            db.session.commit()
            return redirect(url_for('whitelist'))
        else:
            return '<script>alert("The device is already in the list");</script>' 
    except:
        db.session.rollback()
        return '<script>alert("There was an issue adding the device");</script>'

@app.route('/delete/<mac>')
def delete(mac):
    device = Device.query.get_or_404(mac)

    try:
        device.description = 'Unknown device'
        device.registered = False
        db.session.commit()
        return redirect(url_for('whitelist'))
    except:
        db.session.rollback()
        return '<script>alert("There was a problem deleting that device")</script>'

@app.route('/update/<mac>', methods=['GET', 'POST'])
def update(mac):
    device_to_update = Device.query.get_or_404(mac)

    if request.method == 'POST':
        device_to_update.description = request.form['description'] 
        try:
            db.session.commit()
            return redirect('/whitelist')
        except:
            return '<script>alert("There was an issue updating that device")</script>'
    else:
        return render_template('update.html', device = device_to_update)

@app.route('/block/<mac>')
def block(mac):
    device_to_block = Device.query.get_or_404(mac)

if __name__ == '__main__':
    app.run(debug = True)
