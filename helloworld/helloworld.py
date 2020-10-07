import connexion

def greeting(name: str) -> str:
    return 'Hello {name}'.format(name=name)

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/')
    app.add_api('helloworld.yaml', arguments={'title': 'Hello World'})
    app.run()