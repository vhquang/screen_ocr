import re

class Input:

	question = []
	answer = []
	
	def __init__(self):
		fileIn = open('kb.txt', 'r')
		for line in fileIn.readlines():
			q, a = re.split(r'\t+', line)
			self.question.append( q.strip() )
			self.answer.append( a.strip() )
		fileIn.close()


if __name__ == '__main__':
	pass