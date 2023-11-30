def create_module(app, **kwargs):
    from .views import food_bp
    app.register_blueprint(food_bp)

