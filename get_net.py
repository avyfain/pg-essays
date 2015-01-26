import csv
import networkx as nx
from networkx.algorithms import bipartite

def main():
	G=nx.Graph()

	with open('clean_essays.csv', 'rb') as csvfile:
		readerz = csv.reader(csvfile, delimiter=',')
		for row in readerz:
			title = row[0]
			thnx = row[3].replace(' and', ',').replace(', ', ',').split(',')
			people = [x.strip() for x in thnx if (x!=' ' and x!='')]
			G.add_node(title, person=0)
			for p in people:
				if p != 'None':
					G.add_node(p, person=1)
					G.add_edge(p, title)

	print 'Nodes', G.number_of_nodes()
	print 'Edges', G.number_of_edges()

	p_nodes = [n for n,d in G.nodes_iter(data=True) if d['person']==1]
	e_nodes = [n for n,d in G.nodes_iter(data=True) if d['person']==0]
	
	BP = bipartite.projected_graph(G,p_nodes)
	BE = bipartite.projected_graph(G,e_nodes)
	nx.write_gml(BP, 'people.gml')
	nx.write_gml(BE, 'essays.gml')

# def print_nodes(G, kind):
	# p_nodes = [n for n,d in G.nodes_iter(data=True) if d['person']==kind]
# 	p_degrees = [(p, nx.degree(G,p)) for p in p_nodes]
# 	p_degrees.sort(key=lambda tup: tup[1])

# 	for p in reversed(p_degrees):
# 		print p

	#projections

	
	# print 'People', list(people)
	# print 'Essays', list(essays)
	# print 'Degrees', sorted(nx.degree(G).values())

if __name__ == '__main__':
	main()