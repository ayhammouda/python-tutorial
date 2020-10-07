import connexion

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'Log My Messages'})
    app.run()
