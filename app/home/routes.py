from app.home import bp

@bp.route('/', methods=['GET', 'POST'])
def index():
    return "Hello, World! from home"
