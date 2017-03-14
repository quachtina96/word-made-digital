import re
import sys

bullet = '\u2022'
determiners = ["the", "a", "an", "another"]
coordinating_conjunctions = ["for", "nor", "but", "or", "yet", "so"]
prepositions = ["in", "under", "towards", "before"]


def filter_sentence(sentence, exclude_list):
	excluded = set(exclude_list)
	return " ".join([word for word in sentence.split(" ") if word not in excluded])

def replace_with_symbols(text, text_symbol_map):
	raise NotImplementedError

def remove_quotes(text):
	working_text = text
	quote_locs = [m.start() for m in re.finditer('"', text)]

	for i in range(len(quote_locs)-1):
		if i%2 == 0:
			substring = text[quote_locs[i]-1:quote_locs[i+1] +1]
			working_text = working_text.replace(substring, "")
	return working_text

def print_hierarchy(sentence_sets):
	for i in range(len(sentence_sets)):
		sentence_set = sentence_sets[i]
		for j in range(0, len(sentence_set)):
			current_sentence = sentence_set[j]
			if current_sentence != "":
				# Reconstruct sentence to encode hierarchy
				that_indexes = [m.start() for m in re.finditer('that', current_sentence)]
				new_sentence = []
				for i in range(len(current_sentence)):
					if i in that_indexes:
						new_sentence.append("\n\t\t %s %s" %(bullet, current_sentence[i]))
					else:
						new_sentence.append(current_sentence[i])
				new_sentence = ''.join(new_sentence)
				if j == 0:
					print(new_sentence)
				else:	
					print("\t",bulleted(new_sentence))
		print()

def filter_sentences(sentence_set, exclude_list):
	return [filter_sentence(sentence, exclude_list) for sentence in sentence_set]

def bulleted(string):
	return "%s %s" %(bullet, string)

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("You must call program as: python3 bulletpoint.py <datafile>")
        print("This program returns the summarized, bullet-pointed version of the text found in datafile.")
        sys.exit(1)
    filename = sys.argv[1]

	exclude_list = ['has']
	exclude_list.extend(determiners)
	exclude_list.extend(coordinating_conjunctions)
	exclude_list.extend(prepositions)

	f = open(filename, 'r')
	content = f.read()
	removed_quotes = remove_quotes(content)
	paragraphs = removed_quotes.strip().split("\n")
	sentence_sets = [paragraph.strip().split(".") for paragraph in paragraphs]
	filtered = [filter_sentences(sentence_set, exclude_list) for sentence_set in sentence_sets]
	print_hierarchy(filtered)

