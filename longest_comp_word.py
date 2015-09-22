import argparse, csv, heapq

class Node:
	"""Class to represent nodes in a trie"""
	def __init__(self,letter,isEnd=False):
		self.letter = letter
		self.children = [None]*26
		self.isEnd = isEnd

	def __str__(self):
		tmp = "Letter: " + self.letter + " Children: "
		for c in self.children:
			if c is not None:
				tmp += c.letter

		return tmp + " isEnd: " + str(self.isEnd)


class Trie:
	"""Custom class to represent a trie data structure"""

	def __init__(self):
		self.root = Node("")
		self.words = set()

	def __str__(self):
		return self.print_trie(self.root,0)

	# Builds a trie data structure using the words found in fname
	# Assumes that fname is a file with one word per line and that
	# each word contains only lowercase english letters (a-z)
	def build_trie(self,fname):
		with open(fname,'rb') as words_file:
			words_reader = csv.reader(words_file)
			
			for word in words_reader:
				self.words.add(word[0])
				cur = self.root

				for char in word[0]:
					ind = ord(char)-ord('a')

					if cur.children[ind] is None:
						cur.children[ind] = Node(char)
					
					cur = cur.children[ind]

				cur.isEnd = True

	# Helper function to recursively print out the trie
	def print_trie(self,root,depth):
		tmp = "\t"*depth + str(root) + "\n"

		for c in root.children:
			if c is not None:
				tmp += self.print_trie(c,depth+1)

		return tmp

	# Function that returns a list containing all the prefixes of the 
	# given word, including the word itself
	def get_prefixes(self,word):
		prefixes, tmp_prefix, cur = [], "", self.root

		for char in word:
			ind = ord(char)-ord('a')
			if cur.children[ind] is None:
				return prefixes

			cur = cur.children[ind]
			tmp_prefix += char

			if cur.isEnd:
				prefixes.append(tmp_prefix)

		return prefixes


# This function finds the longest compound word in words using the trie
# passed in as an argument.
# 
# words should be a standard python set and trie should be a Trie data
# structure as defined above
def find_longest(words, trie):
	# Initialize heap and a 'considered' set to prevent unecessary computation
	heap, considered = [], set()

	# Iterate through starting set of words, adding all prefixes into the heap
	for w in words:
		prefixes = trie.get_prefixes(w)
		for p in prefixes:
			if len(p) != len(w):
				heap.append((-len(w), w, w[len(p):]))
				considered.add(w[len(p):])

	# Create a min-heap whose elements are 3-tuples (l,orig,suff) where
	# l is -(length of the original word), orig is the original word, and 
	# suff is the suffix of the orginal word. We define l as is because 
	# the heapq module only implements a min-heap
	heapq.heapify(heap)
	while heap:
		l,orig,suff = heapq.heappop(heap)
		
		# Quickly check if the suffix is in the set of words given.
		# Else, consider prefixes of the word. Using the min-heap allows us
		# to immediately return the first result we find since we access the 
		# words in order of their length
		if suff in words:
			return orig
		else:
			prefixes = trie.get_prefixes(suff)
			for p in prefixes:
				new_suff = suff[len(p):]
				if len(p) != len(suff) and new_suff not in considered:
					heapq.heappush(heap,(l,orig,new_suff))
					considered.add(new_suff)


# Main function
def main():
	# Parser interprets command line 
	parser = argparse.ArgumentParser(description='Finds the longest compound \
		word in the given list of words')
	parser.add_argument('filename', metavar='fname',type=str,help='File name \
		containing word list')
	args = parser.parse_args()

	# Build trie and execute function to find longest compound word
	trie = Trie()
	trie.build_trie(args.filename)
	result = find_longest(trie.words,trie)

	if result is not None:
		print result
	else:
		print "No compound words"

if __name__ == '__main__':
	main()