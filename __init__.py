# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import LOG
from SPARQLWrapper import SPARQLWrapper, JSON
from string import Template

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

LOGGER = LOG(__name__)

# TODO: Change "Template" to a unique name for your skill
class MusicBrainzSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(MusicBrainzSkill, self).__init__(name="MusicBrainzSkill")
        # Initialize working variables used within the skill.
        self.performer = "I do not know who sings that"

    def initialize(self):
        song_intent = IntentBuilder("SongIntent").require("Who").require("Have").require("Song").require("SongNameTest").build()
        self.register_intent(song_intent, self.handle_who_is_singing_intent)


    def handle_who_is_singing_intent(self, message):
        
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""PREFIX schema: <http://schema.org/>
                        select ?name
                        FROM <https://broker.semantify.it/graph/OH172BSiiG/Wy7u0ZjcOA/2018-10-11-17-20>
                        where { 
	                        ?s a schema:MusicRecording.
                            ?s schema:byArtist ?artist.
                            ?s schema:name "$name" .
                            ?artist schema:name ?name 
                        } """)

        sparql.setQuery(qt.substitute(name=message.data["SongNameTest"]))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
           self.performer = result["name"]["value"]

        self.speak_dialog("sung.by", data={"performer": self.performer})


    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return MusicBrainzSkill()
