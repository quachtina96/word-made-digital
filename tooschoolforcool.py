#!/usr/bin/python
# Through the Park
# A 1k story generator (excluding comments) that uses only elision
# Nick Montfort, 2008-2009
# Thanks to Michael Mateas & Beth Cardier
# JavaScript version: http://nickm.com/poems/through_the_park.html

import random, textwrap


school = ["Everything slows",
"The girl grasps for flimsy pages",
"The girl sighs",
"The girl strokes her chin",
"The pages rustle",
"The girl looks up at the clock",
"The tutor paces the girl",
"Locution after locution",
"The tutor makes a fist behind his back",
"A tape recorder spins, tightly gripped",
"It reminds the girl of her grandmother",
"'Stop complaining!'",
"He encourages her",
"'Keep going...'",
"He urges her",
"'No'",
"'Yes'",
"They exchange a knowing glance",
"The two circle the words",
"Something sits in the air",
"Her breathing quickens",
"Locutions fails to form meaning",
"The girl dashes, leaving words behind",
"Thoughts scatter",
"Understanding settles",
"The girl races",
"The man's there first",
"Things are forgotten in carelessness"]

school = ["Everything slows",
"The girl grasps for flimsy pages",
"The girl sighs",
"The girl strokes her chin",
"The pages rustle",
"The girl looks up at the clock",
"The tutor paces the girl",
"Locution after locution",
"The tutor makes a fist behind his back",
"A tape recorder spins, tightly gripped",
"It reminds the girl of her grandmother",
"'Stop complaining!'",
"He encourages her",
"'Keep going...'",
"He urges her",
"'No'",
"'Yes'",
"They exchange a knowing glance",
"The two circle the words",
"Something sits in the air",
"Her breathing quickens",
"Locutions fails to form meaning",
"The girl dashes, leaving words behind",
"Thoughts scatter",
"Understanding settles",
"The girl races",
"The man's there first",
"Things are forgotten in carelessness"]

#source: https://www.reddit.com/r/OneParagraph/comments/5twii8/the_silence_is_deafening/
# The Train
reddit = [ "Sunset colors the sky.", "A train's horn blows in the distance", "A bike's bell dings next door", "A car screeches on the driveway", "I know that she is coming round", "I want to prepare a welcome", "Where will she take me next?" ,"The sound of her wheels turning", "","They churn and churn in my head", "I try to focus", "If only he came too.", "The train roars through", "How did it come to this?", "Who let that train get out of control?", "It's gone for now.", "But I know she'll be back again.", "The familiar smoke and the warmth of home.","Please stop this train.", "Sunset colors the sky.", "Darkness follows.", "Does the train sleep?" ]

text = reddit

while len(text) > 7:
    text.remove(random.choice(text))
print "\nThe Train\n"
print textwrap.fill(". ... ".join(text) + ".", 80)
