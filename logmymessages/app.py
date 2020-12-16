import connexion

def health_check():
    return {}

app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/')
app.add_api('swagger.yaml', arguments={'title': 'Log My Messages'})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
