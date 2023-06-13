from flask import Flask
from flask_restful import Api
from api.config import AppConfig


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(AppConfig)

    from api.main import (
        Get_Match_by_id, 
        Get_All_Matches,
        Add_Team,
        Add_Player,
        Start_New_Match,
        Update_Match_points,
        Get_All_Players,
        Get_Player_By_Id,
        Get_Team_By_Id,
        Get_All_Team)

    api.add_resource(Start_New_Match,'/match') # POST
    api.add_resource(Get_All_Matches,'/match') # GET
    api.add_resource(Get_Match_by_id,'/match/<int:id>') # GET
    api.add_resource(Update_Match_points,'/match/<int:id>') # PATCH

    api.add_resource(Add_Player, '/player') # POST
    api.add_resource(Get_All_Players,'/player') # GET
    api.add_resource(Get_Player_By_Id,'/player/<int:id>') # GET

    api.add_resource(Add_Team, '/team') # POST
    api.add_resource(Get_All_Team,'/team') # GET
    api.add_resource(Get_Team_By_Id,'/team/<int:id>') # GET
    
    return app