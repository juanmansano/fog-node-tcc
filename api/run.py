from fog_api import create_app, create_mqtt_connection

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5210, debug = True)
