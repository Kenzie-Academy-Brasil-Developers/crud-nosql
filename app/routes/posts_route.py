from app.controllers import post_controller


def posts_route(app):
    @app.get("/posts")
    def retrieve():
        return post_controller.read_posts()

    @app.post("/posts")
    def create_posts():
        return post_controller.create_post()
    
    @app.get("/posts/<int:id>")
    def read_posts_by_id(id):
        return post_controller.read_post_by_id(id)
    
    @app.delete("/posts/<int:id>")
    def delete_posts(id):
        return post_controller.remove_post(id)
    
    @app.patch("/posts/<int:id>")
    def update_posts(id):
        return post_controller.update_post(id)