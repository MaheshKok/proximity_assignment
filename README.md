Project Structure:
all models can be found under application > models
all schemas can be found under application > schemas
all Apis can be found under application > blueprints > apis
all Test stories can be found under application >  tests > unit_test > test_stories
it will give you Crystal Clear idea as how stories are implemented

Events:
i have used sqlalchemy events to update view_count on update (requirement is not clear as when the view_count will increase)


Tools and Frameworks
Framework : flask_rest_json_api for API building (many in built functions like searching, sorting, very fast and easy to implement)
database: Postgresql ( as its relational database postgres is very powerful as compared with other databases)
ORM : SqlAlchmey (one of the most powerful ORM in the market)
Serialization and Deserialization: Marshmallow_json (cant think of any other library doing better job)
unit test: pytest (light weight and supports many features)
logging: python default logging (in future implement sentry. one of the best service to tract exceptions and logs)


should have implemented:
Docker: i should have used docker but due to time constraint and limited knowledge didnt go for it
its nothing like i cant do it, but it needs a lil bit of research 
