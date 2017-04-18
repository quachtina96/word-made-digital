poemText = `When Simone Weil said it would be wrong
to think the mystics borrow the language of love
for it is theirs by right, though she didn’t call it
the heavenly song of cock and cunt, perhaps that’s
the inevitable conclusion of the sacred heart wounded
into a womb, an arrow in the hand of an angel
piercing such a depth in the body until it’s beyond
what the body knows, delirious among the lilies
or tasting the sweet meats of that table. Yet
whoever the mystic woman is, she’s not ‘about’
sex; it’s not some sexual fantasy that she lies with
in the dark mansion of God, sleeping every night
in a different room, curling herself to the different shapes
of emptiness. It’s not some narrative of first
he this, then she that, that makes her tremble,
being naked and open to nothing but that
noche oscura, when with love inflamed,
the saint runs out of the house into the hills,
for she remains, asleep and dreaming, and in God’s
innumerable rooms, innumerable forms and shapes
of love, she lies down with them all in the depths
of her body and blood, until every vision and icon
shines with a glimpse of the forgotten and atavistic
feminine body, pouring out of her as if out of the nipple
of that blue stone embedded in the miraculous
hand, as she herself becomes her own threshold;
no faces remembered or imagined flicker across the hymen
of her mind, for it’s not a penis, even God’s, that she imagines,
but the form of herself, the knowing of the body
of her own feeling, as in the Old Testament it was said
that Jacob knew Rachel or Lot knew his own daughters,
the knowing of the body allowed only to men;
women, only the known or unknown, as she is known and un-
known but as she knows herself as she knows the other
that she is not: she enters herself, with fingers
 of melting wax, of cold cucumber, with a thumb
of glow, with all the abandoned utensils
of domestic life, with a stalk from the forsaken
garden, and with the lost wing feather of the angel
of death and with the voice of a baby’s cry
nursing on the vestigial milk of the mother of mercy.`

proseText = `The idea of being able to become invisible, especially by simply covering up a person or an object with a special cloak, has a perennial appeal in science-fiction and fantasy literature. In recent years, researchers have found ways to make very exotic “metamaterials” that can perform a very crude version of this trick, keeping an object from being detected by a certain specific frequency of radiation, such as microwaves, and only working at microscopic scales. But a system that works in ordinary visible light and for objects big enough to be seen with the naked eye has remained elusive.
Now, a team of researchers in the Singapore-MIT Alliance for Research and Technology (SMART) Centre has found a relatively simple, inexpensive system that can hide an object as big as a peppercorn from view in ordinary visible light. The team’s discovery has been published online in Physical Review Letters and will appear soon in the print version of the journal.
Unlike the other attempts to produce invisibility by constructing synthetic layered materials, the new method uses an ordinary, common mineral called calcite — a crystalline form of calcium carbonate, the main ingredient in seashells. “Very often, the obvious solution is just sitting there,” says MIT mechanical-engineering professor George Barbastathis, one of the new report’s co-authors.
The paper was co-authored by SMART postdoctoral fellow Baile Zhang, MIT postdoctoral fellow Yuan Luo, and SMART researcher Xiaogang Liu, and the research was funded by Singapore’s National Research Foundation (NRF) and the U.S. National Institutes of Health (NIH).
In the experiment reported in this paper, the system works in a very carefully controlled setting: The object to be hidden (a metal wedge in the experiment, or anything smaller than it) is placed on a flat, horizontal mirror, and a layer of calcite crystal — made up of two pieces with opposite crystal orientations, glued together — is placed on top of it. When illuminated by visible light and viewed from a certain direction, the object under the calcite layer “disappears,” and the observer sees the scene as if there was nothing at all on top of the mirror.
For their demonstration, they placed the MIT logo upside-down on the vertical wall behind the apparatus, placed so that one of the letters could be viewed directly via the mirror, while the other two were behind the area with a 2-millimeter-high wedge (the height of a peppercorn) and its concealing layer of calcite. Then, the whole setup was submerged in liquid. They showed that the logo appeared normal, as though there was no wedge but a flat mirror piece, when illuminated with visible green light. Any imperfection in the cloaking effect would have shown up as a misalignment of the letters, but there was no such anomaly; thus, the cloaking operation was proven. With blue or red illumination, the cloaking was still effective but with some slight misalignment.`

var insertText = function(sampleType, displayAreaID) {
	if (sampleType == 'poem') {
		text = poemText
	} else {
		text = proseText
	}
	document.getElementById('inputArea').value = text
}

var mosaic = function(displayAreaID, inputDiv) {
	console.log('hihihi')
	document.getElementById(inputDiv).style.display = "none";
	currentText = document.getElementById(displayAreaID).value
	$.ajax({
	  type: "POST",
	  url: "mosaic.py",
	  data: { param: currentText}
	}).done(function(o) {
	   // do something
	});
}

var reset = function(inputDiv, mosaicDiv) {
	document.getElementById(inputDiv).style.display = "block";
	document.getElementById(mosaicDiv).style.display = "none";
}


