from __future__ import division
import igraph as ig
from datetime import datetime, timedelta
import json


# Function to add new nodes and edges to graph
def add_nodes(tag):
    if len(tag[0]) == 1:
        return None
    new_time = tag[1]
    new_nodes = []
    to_add = []
    edge_len = len(g.es)
    if new_time >= max_time:
        for key in tag[0]:  # tag[0] are the hashtags in the current tweet
            if key in g.vs['name']:
                pass
            else:
                new_nodes.append(key)
                g.add_vertices(key)

    # This will pick out the ones that are new, and pair with existing nodes
    for i in tag[0]:
        for j in new_nodes:
            if j != i:
                if i in new_nodes:
                    pass
                else:
                    to_add.append([i,j])




    itr = []
    for i in tag[0]:
        for j in new_nodes:
            if i != j:
                if (j,i) in itr:
                    pass
                else:
                    itr.append((i,j))
                    g.add_edges([(i, j)])



    # This then adds edges between new nodes and relevant existing nodes
    for i in to_add:
        g.add_edges([i])


    # Add timestamps to edges
    for i in range(edge_len, edge_len+(len(g.es)-edge_len)):
        g.es[i]['timestamp'] = tag[1]










# Create initial graph
g = ig.Graph()


# This is how the first line of the file will be read, before iterating over the entire file and using the function to add nodes
# This is done to initialize the graph with hashtags.
with open('./tweet_input/tweets.txt') as f:
    for line in f:
        data1 = json.loads(line)
        if len(data1['entities']['hashtags']) == 0:  # This will keep searching until the first tweet with hashtags is found
            pass
        else:
            time = datetime.strptime(data1['created_at'][:19], '%a %b %d %H:%M:%S')
            tags = []
            for i in range(0, len(data1['entities']['hashtags'])):
                tags.append(str(data1['entities']['hashtags'][i]['text']))

            tag_time = tags, time

            max_time = tag_time[1]

            g.add_vertices(tag_time[0])

            itr = []
            for i in tag_time[0]:
                for j in tag_time[0]:
                    if i != j:
                        if (j,i) in itr:
                            pass
                        else:
                            itr.append((i,j))
                            g.add_edges([(i, j)])


            for i in range(0, len(g.es)):
                g.es['timestamp'] = time

            break







# This is how each line of the file will be read
with open('./tweet_input/tweets.txt') as data_file:
    for line in data_file:
        try:
            data = json.loads(line)

            time = datetime.strptime(data['created_at'][:19], '%a %b %d %H:%M:%S')
            tags = []
            for i in range(0, len(data['entities']['hashtags'])):
                tags.append(data['entities']['hashtags'][i]['text'])


            tag_time = tags, time

            new_time = tag_time[1]
            if new_time > max_time:
                max_time = new_time

            add_nodes(tag_time)


            if len(g.es) != 0:
                avg_degree = round(sum(g.degree())/len(g.degree()), 2)
                with open('./tweet_output/output.txt', 'a') as output:
                    output.write('%.2f' % avg_degree)  # This will have it always print out to two decimal places
                    output.write('\n')


        except KeyError:
            pass

        # This removes edges older than 60s from the current tweet used in the graph:
        try:
            for i in range(0, len(g.es)):
                if tag_time[1] > g.es[i]['timestamp'] + timedelta(seconds=60):
                    g.delete_edges(g.es[i])

            for i in g.vs['name']:
                if g.degree(i) == 0:
                    g.delete_vertices(i)
        except IndexError:
            pass
