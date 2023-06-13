from flask_restful import Resource, reqparse, abort
from flask import jsonify
from api.config import MySqlDatabase
import json




# GET DETAILS OF MATCH BY IT's ID
class Get_Match_by_id(Resource):
    def get(self, id):
        cursor, db = MySqlDatabase.connection()
        cursor.execute("""  SELECT m.*, CONCAT("[",GROUP_CONCAT(JSON_OBJECT(
                                        "team_id",  team_has_match.team_id,
                                        "team_plyers", (
                                        SELECT CONCAT("[",GROUP_CONCAT(player.player_name),"]") as players
                                        FROM player_has_team
                                        JOIN player ON player.player_id = player_has_team.player_id  
                                        WHERE player_has_team.team_id = team_has_match.team_id group by player_has_team.team_id
                                        ),
                                "points", team_has_match.points
                                )),"]") AS team_data
                            FROM `match` m
                            JOIN team_has_match ON team_has_match.match_id = m.match_id 
                            WHERE m.match_id = %s group by team_has_match.match_id;""",(id,))
        match = cursor.fetchone()
        match['team_data'] = json.loads(match['team_data'])
        MySqlDatabase.close_connection(cursor, db)
        return jsonify({'match':match})



# START NEW MATCH
start_new_match_parse = reqparse.RequestParser()
start_new_match_parse.add_argument('number_of_sets',type=str, required=True, help='number of sets is required')
start_new_match_parse.add_argument('team_1',type=int, required=True, help='Team 1 is required')
start_new_match_parse.add_argument('team_2',type=int, required=True, help='Team 2 is required')
class Start_New_Match(Resource):
    
    def post(self):
        args = start_new_match_parse.parse_args()
        number_of_sets = args['number_of_sets']
        team_1 = args['team_1']
        team_2 = args['team_2']

        # Check If Team Exist
        if team_1:
            cursor, db = MySqlDatabase.connection()
            cursor.execute("""
                            SELECT * FROM team WHERE team_id=%s;
                            """,(team_1,))
            get_team_1 = cursor.fetchone()

            if not get_team_1:
                MySqlDatabase.close_connection(cursor, db)
                abort(http_status_code=406,message=f"You have passed invalid team id")
        
        # Check If Team Exist
        if team_2:
            cursor, db = MySqlDatabase.connection()
            cursor.execute("""
                            SELECT * FROM team WHERE team_id=%s;
                            """,(team_2,))
            get_team_2 = cursor.fetchone()

            if not get_team_2:
                MySqlDatabase.close_connection(cursor, db)
                abort(http_status_code=406,message=f"You have passed invalid team id")



        cursor, db = MySqlDatabase.connection()
        cursor.execute("""
                        INSERT INTO `match`(number_of_sets) VALUE(%s);
                        """,(number_of_sets,))
        match_id = cursor.lastrowid
        db.commit()
        
        cursor.execute("""
                        INSERT INTO team_has_match(team_id, match_id) VALUE(%s,%s);
                        """,(team_1,match_id))
        db.commit()

        cursor.execute("""
                        INSERT INTO team_has_match(team_id, match_id) VALUE(%s,%s);
                        """,(team_2,match_id))
        db.commit()
        MySqlDatabase.close_connection(cursor, db)
        message = "New match added successfully!"
        return jsonify({"status":201,"message":message, "match_id": match_id})



# GET DETAILS OF ALL MATCHES
class Get_All_Matches(Resource):
    def get(self):
        cursor, db = MySqlDatabase.connection()
        cursor.execute("""  SELECT m.*, CONCAT('[',GROUP_CONCAT(JSON_OBJECT(
                                        'team_id',  team_has_match.team_id,
                                        'team_plyers', (
                                        SELECT CONCAT('[',GROUP_CONCAT(player.player_name),']') as players
                                        FROM player_has_team
                                        JOIN player ON player.player_id = player_has_team.player_id  
                                        WHERE player_has_team.team_id = team_has_match.team_id group by player_has_team.team_id
                                        ),
                                'points', team_has_match.points
                                )),']') AS team_data
                            FROM `match` m
                            JOIN team_has_match ON team_has_match.match_id = m.match_id 
                            group by team_has_match.match_id;""")
        matchs = cursor.fetchall()
        MySqlDatabase.close_connection(cursor, db)
        for match in range(len(matchs)):
            matchs[match]['team_data'] = json.loads(matchs[match]['team_data'])
        
        return jsonify({'match':matchs})
    


# UPDATE MATCH STORE
update_match_points_parse = reqparse.RequestParser()
update_match_points_parse.add_argument('points',type=int, required=True, help='Points is required')
update_match_points_parse.add_argument('team_id',type=int, required=True, help='Team ID is required')
class Update_Match_points(Resource):
    def patch(self, id):

        # Check If Match Exist
        if id:
            cursor, db = MySqlDatabase.connection()
            cursor.execute("""
                            SELECT * FROM `match` WHERE match_id=%s;
                            """,(id,))
            get_match_id = cursor.fetchone()

            if not get_match_id:
                MySqlDatabase.close_connection(cursor, db)
                abort(http_status_code=406,message=f"You have passed invalid match id")


        args = update_match_points_parse.parse_args()
        points = args['points'] 
        team_id = args['team_id']

        # Check If team Exist
        if team_id:
            cursor, db = MySqlDatabase.connection()
            cursor.execute("""
                            SELECT * FROM team_has_match WHERE team_id=%s AND match_id=%s;
                            """,(team_id,id,))
            get_match_team_id = cursor.fetchone()

            if not get_match_team_id:
                MySqlDatabase.close_connection(cursor, db)
                abort(http_status_code=406,message=f"You have passed invalid team_id id")

        cursor, db = MySqlDatabase.connection()
        cursor.execute("""
                        UPDATE team_has_match SET points = %s
                        WHERE match_id=%s AND team_id=%s;
                        """,(points,id,team_id,))
        db.commit()
        MySqlDatabase.close_connection(cursor, db)
        message = "Match Scores Updated successfully!"
        return jsonify({"status":201,"message":message, "match_id": id})


# ADD NEW PLAYERS 
add_player_parse = reqparse.RequestParser()
add_player_parse.add_argument('player_name', type=str, required=True, help='player name is required')
class Add_Player(Resource):
    def post(self):
        args = add_player_parse.parse_args()
        player_name = args['player_name']

        cursor, db = MySqlDatabase.connection()
        cursor.execute("""
                        INSERT INTO player(player_name) VALUE(%s);
                        """,(player_name,))
        player_id = cursor.lastrowid
        db.commit()
        MySqlDatabase.close_connection(cursor, db)
        message = "New Player added successfully!"
        return jsonify({"status":201,"message":message, "player_created":{"player_id":player_id, "player_name": player_name}})


# GET ALL PLAYERS
class Get_All_Players(Resource):
    def get(self):
        cursor, db = MySqlDatabase.connection()
        cursor.execute("""
                        SELECT p.player_name, p.player_id, COUNT(m.match_id) AS matches_played
                        FROM player p
                        LEFT JOIN player_has_team pt ON p.player_id = pt.player_id
                        LEFT JOIN team t ON pt.team_id = t.team_id
                        LEFT JOIN team_has_match tm ON t.team_id = tm.team_id
                        LEFT JOIN `match` m ON tm.match_id = m.match_id
                        GROUP BY p.player_id;
                        """)
        all_players = cursor.fetchall()
        MySqlDatabase.close_connection(cursor, db)
        return jsonify({"status":200,"all_players":all_players})



# GET PLAYER BY ID
class Get_Player_By_Id(Resource):
    def get(self, id):
        cursor, db = MySqlDatabase.connection()
        cursor.execute("""
                        SELECT p.player_name, p.player_id, COUNT(m.match_id) AS matches_played
                        FROM player p
                        LEFT JOIN player_has_team pt ON p.player_id = pt.player_id
                        LEFT JOIN team t ON pt.team_id = t.team_id
                        LEFT JOIN team_has_match tm ON t.team_id = tm.team_id
                        LEFT JOIN `match` m ON tm.match_id = m.match_id
                        WHERE p.player_id = %s
                        GROUP BY p.player_id;
                        """,(id,))
        player = cursor.fetchone()
        MySqlDatabase.close_connection(cursor, db)
        return jsonify({"status":200,"player":player})
    


# ADD NEW TEAM 
add_team_parse = reqparse.RequestParser()
add_team_parse.add_argument('team_name', type=str, required=True, help='team name is required')
add_team_parse.add_argument('player_1', type=int, required=False, help='player 1 id is required')
add_team_parse.add_argument('player_2', type=int, required=False, help='player 2 id')
class Add_Team(Resource):
    def post(self):
        args = add_team_parse.parse_args()

        team_name = args['team_name']
        player_1 = args['player_1'] if args['player_1'] else None
        player_2 = args['player_2'] if args['player_2'] else None

        # Check if player_1 exist
        if player_1:
            cursor, db = MySqlDatabase.connection()
            cursor.execute("""
                            SELECT * FROM player WHERE player_id=%s;
                            """,(player_1,))
            get_player_1 = cursor.fetchone()

            if not get_player_1:
                MySqlDatabase.close_connection(cursor, db)
                abort(http_status_code=406,message=f"You have passed invalid player id")

        # Check if player_2 exist
        if player_2:
            cursor, db = MySqlDatabase.connection()
            cursor.execute("""
                            SELECT * FROM player WHERE player_id=%s;
                            """,(player_2,))
            get_player_2 = cursor.fetchone()

            if not get_player_2:
                MySqlDatabase.close_connection(cursor, db)
                abort(http_status_code=406,message=f"You have passed invalid player id")

        
        # Check if team already exist with same players
        if player_1 and player_2:
            cursor, db = MySqlDatabase.connection()
            cursor.execute("""
                        SELECT p1.team_id, p1.player_id as player1, p2.player_id as player2 FROM player_has_team p1
                        JOIN player_has_team p2 ON p1.player_id <> p2.player_id
                        WHERE p1.player_id = %s AND p2.player_id = %s
                        AND p1.team_id = p2.team_id;
                        """,(player_1,player_2,))
            
            team_already_exist = cursor.fetchone()
            if team_already_exist:
                MySqlDatabase.close_connection(cursor, db)
                abort(http_status_code=406,message="Team With Same Players Already Exist ", team_id=team_already_exist['team_id'])

        if team_name: 
            cursor, db = MySqlDatabase.connection()
            cursor.execute("""
                        INSERT INTO team(team_name) VALUE(%s);
                        """,(team_name,))
            team_id = cursor.lastrowid
            db.commit()

            cursor.execute("""
                        INSERT INTO player_has_team(player_id, team_id) VALUE(%s,%s);
                        """,(player_1,team_id,))
            
            if player_2 != None:
                cursor.execute("""
                        INSERT INTO player_has_team(player_id, team_id) VALUE(%s,%s);
                        """,(player_2,team_id,))
            db.commit()
            MySqlDatabase.close_connection(cursor, db)
            message = "New team added successfully!"
            return jsonify({"status":201,"message":message, "team_created":{"player_id":team_id, "team_name": team_name}})


# GET TEAM BY ID
class Get_Team_By_Id(Resource):
    def get(self, id):
        cursor, db = MySqlDatabase.connection()
        cursor.execute("""
                        SELECT t.team_name , COUNT(tm.match_id) AS matches_played
                        FROM team t
                        LEFT JOIN team_has_match tm ON t.team_id = tm.team_id
                        WHERE t.team_id = %s
                        GROUP BY t.team_id;
                        """,(id,))
        team = cursor.fetchone()
        MySqlDatabase.close_connection(cursor, db)
        return jsonify({"status":200,"team":team})
    

# GET ALL TEAMS
class Get_All_Team(Resource):
    def get(self):
        cursor, db = MySqlDatabase.connection()
        cursor.execute("""
                        SELECT t.team_id, t.team_name , COUNT(tm.match_id) AS matches_played
                        FROM team t
                        LEFT JOIN team_has_match tm ON t.team_id = tm.team_id
                        GROUP BY t.team_id;
                        """)
        all_teams = cursor.fetchall()
        MySqlDatabase.close_connection(cursor, db)
        return jsonify({"status":200,"all_teams":all_teams})
    

