import sys

from application.app import Application
from application.validate import validate_input

if __name__ == '__main__':
    try:
        validate_input(sys.argv)
    except ValueError as e:
        sys.stdout.write(str(e) + "\n")
        sys.exit(1)
    app = Application(int(sys.argv[1]))
    try:
        app.run()
    except Exception as e:
        sys.stdout.write(str(e) + "\n")
    finally:
        app.close()
