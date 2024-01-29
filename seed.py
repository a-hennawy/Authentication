from models import User, db, Feedback
from app import app

db.drop_all()
db.create_all()

user1 = User.register("big_ben", "1234567",
                      "bigboyben97@gmail.com",
                       "Big", "Ben" )
user2 = User.register("a_hennawy", "1234567",
                      "ahmed97@gmail.com",
                       "Ahmed", "Hennawy" )
user3 = User.register("nosha_123", "1234567",
                      "nosha@hotmail.com", 
                       "Noor","Al-Jamea" )

db.session.add_all([user1, user2, user3])
db.session.commit()

feedback1 = Feedback(title="reviews", content="all reviews good!!", username="big_ben")
feedback2 = Feedback(title="Homepage", content="i like the design of the homepage", username="big_ben")
feedback3 = Feedback(title="reviews", content="all reviews good!!", username="a_hennawy")
feedback4 = Feedback(title="Homepage", content="i like the design of the homepage", username="a_hennawy")

db.session.add_all([feedback1, feedback2, feedback3, feedback4])
db.session.commit()

db.session.add_all