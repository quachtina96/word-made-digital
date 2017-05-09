import random
# code from https://gist.github.com/agiliq/131679
# adapted by Tina Quach

class Markov(object):
	
	def __init__(self, text):
		self.cache = {}
		self.words = text.split()
		self.word_size = len(self.words)
		self.database(self.words)	
		
	def triples(self, words):
		""" Generates triples from the given data string. So if our string were
				"What a lovely day", we'd generate (What, a, lovely) and then
				(a, lovely, day).
		"""
		
		if len(words) < 3:
			return
		
		triples = []
		for i in range(len(words) - 2):
			triples.append((words[i], words[i+1], words[i+2]))
		return triples
			
	def database(self, words):
		for w1, w2, w3 in self.triples(words):
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]

	def update(self, text):
		words = text.split()
		self.words = self.words + words
		threes = self.triples(words)
		self.database(threes)
				
	def make_sentence(self, size=10):
		seed = random.randint(0, self.word_size-3)
		seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word, next_word
		gen_words = []
		for i in xrange(size):
			gen_words.append(w1)
			if (w1, w2) in self.cache:
				w1, w2 = w2, random.choice(self.cache[(w1, w2)])
			else:
				w1, w2 = random.choice(random.choice(self.cache.values())), random.choice(random.choice(self.cache.values()))
		gen_words.append(w2)
		return ' '.join(gen_words)
	
def test():		
	m = Markov(open('EC-Marked/tina_ec.txt','r').read())
	for i in range(10):
		print(m.generate_markov_text())
	boop = """When Simone Weil said it would be wrong
	to think the mystics borrow the language of love
	for it is theirs by right, though she didn't call it
	the heavenly song of cock and cunt, perhaps that's
	the inevitable conclusion of the sacred heart wounded
	into a womb, an arrow in the hand of an angel
	piercing such a depth in the body until it's beyond
	what the body knows, delirious among the lilies
	or tasting the sweet meats of that table. Yet
	whoever the mystic woman is, she's not 'about'
	sex; it's not some sexual fantasy that she lies with
	in the dark mansion of God, sleeping every night
	in a different room, curling herself to the different shapes
	of emptiness. It's not some narrative of first
	he this, then she that, that makes her tremble,
	being naked and open to nothing but that
	noche oscura, when with love inflamed,
	the saint runs out of the house into the hills,
	for she remains, asleep and dreaming, and in God's
	innumerable rooms, innumerable forms and shapes
	of love, she lies down with them all in the depths
	of her body and blood, until every vision and icon
	shines with a glimpse of the forgotten and atavistic
	feminine body, pouring out of her as if out of the nipple
	of that blue stone embedded in the miraculous
	hand, as she herself becomes her own threshold;
	no faces remembered or imagined flicker across the hymen
	of her mind, for it's not a penis, even God's, that she imagines,
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
	of death and with the voice of a baby's cry
	nursing on the vestigial milk of the mother of mercy."""
	m.update(boop.decode('utf-8').strip())
	for i in range(10):
		print(m.generate_markov_text())
