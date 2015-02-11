import csv
import networkx as nx
from networkx.algorithms import bipartite
# import matplotlib.pyplot as plt

def main():
	G=nx.Graph()

	with open('clean_essays.csv', 'rb') as csvfile:
		readerz = csv.reader(csvfile, delimiter=',')
		for row in readerz:
			title = row[0]
			thnx = row[3].replace(' and', ',').replace(', ', ',').split(',')
			people = [x.strip() for x in thnx if (x!=' ' and x!='')]
			G.add_node(title, klass='essay')
			for p in people:
				if p != 'None':
					G.add_node(p, klass='person')
					G.add_edge(p, title)

	p_nodes = [n for n,d in G.nodes_iter(data=True) if d['klass']=='person']
	e_nodes = [n for n,d in G.nodes_iter(data=True) if d['klass']=='essay']
	
	BP = bipartite.projected_graph(G,p_nodes)
	BE = bipartite.projected_graph(G,e_nodes)
	nx.write_gml(BP, 'people.gml')
	nx.write_gml(BE, 'essays.gml')
	print "Done"

if __name__ == '__main__':
	main()


