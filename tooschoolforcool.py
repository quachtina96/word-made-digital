#!/usr/bin/python
# Through the Park
# A 1k story generator (excluding comments) that uses only elision
# Nick Montfort, 2008-2009
# Thanks to Michael Mateas & Beth Cardier
# JavaScript version: http://nickm.com/poems/through_the_park.html

import random, textwrap
text = ["Everything slows",
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
"'Turn those lemons into lemonade!'",
"He encourages her",
"'Keep going...'",
"He urges her",
"'No, those are melons...'",
"They exchange a knowing glance",
"The two circle the words",
"Something weaves through the air",
"Her breathing quickens",
"Locutions fails to form meaning",
"The girl dashes, leaving words behind",
"Thoughts scatter",
"The girl races",
"The man's there first",
"Things are forgotten in carelessness",
"She gapes"]
while len(text) > 7:
    text.remove(random.choice(text))
print "\nToo School for Cool\n\n" + \
    textwrap.fill(". ... ".join(text) + ".", 80)
