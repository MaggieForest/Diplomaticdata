# -*- coding: utf-8 -*-
 
#from django.http import HttpResponse
from django.shortcuts import render

from django.http import HttpResponse

from py2neo import Graph,Node,Relationship,database

from django.core   import serializers

import json

import numpy as np

test_graph = Graph(
    "http://127.0.0.1:7474",
    username="neo4j",
    password="77777"
)

def f2(a,b):
    return b['val']-a['val']

def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)

def near(request):
    return render(request,'near.html')

def find_near(request):
    a = request.GET['pname']
    data = test_graph.data("Match (n:Person{name: {str}})-[r:CALL]-(end:Person) where r.value > 1 return r.value, "
                           "n.name,end.name order by r.value desc limit 25",str=a)
    '''
    for i in data:
        iname = i['end.name']
        #inode = test_graph.node(i['end.id'])
        for j in data:
            jname = j['end.name']
            if iname==jname:
                continue
            #jnode = test_graph.node(j['end.id'])
            #find_r = test_graph.match_one(start_node=inode,end_node=jnode,bidirectional=True);
            find_r = test_graph.data("Match (n:Person{name: {i}})-[r:CALL]-(end:Person{name:{j}}) return r.value",i=iname
                                     ,j=jname)
            if find_r:
                data.append({"r.value":find_r[0]['r.value'],"n.name":iname,"end.name":jname})
    '''
    '''

    for i in range(0, len(data)):
        hisdata = test_graph.data(
            "Match (n:Person{name: {str}})-[r:CALL]-(end:Person) where r.value > 10 return r.value, "
            "n.name,end.name order by r.value desc limit 25", str=data[i]['end.name'])
        for j in range(0, len(hisdata)):
            if hisdata[j]['end.name'] == data[i]['end.name']:
                data.append(hisdata[j])
    '''
    hisdatas = []
    for i in range(0, len(data)):
        hisdata = test_graph.data(
            "Match (n:Person{name: {str}})-[r:CALL]-(end:Person) where r.value > 100 return r.value, "
            "n.name,end.name", str=data[i]['end.name'])
        hisdatas.append(hisdata)

    cnt = 0
    for i in range(0, len(data)):
        for j in range(0, len(hisdatas)):
            for k in range(0, len(hisdatas[j])):
                if (data[i]['end.name'] == hisdatas[j][k]['end.name']):
                    if (hisdatas[j][k] in data):
                        continue
                    else:
                        data.append({'r.value': hisdatas[j][k]['r.value'], 'n.name': hisdatas[j][k]['end.name'],
                                     'end.name': hisdatas[j][k]['n.name']})
                        # cnt += 1
    # print cnt

    return HttpResponse(json.dumps(data),content_type="application/json")

def path(request):
    return render(request,'path.html')

def find_path(request):
    #return render(request,'path.html')
    fperson = request.GET['fname']
    tperson = request.GET['tname']
    data = test_graph.run("Match(p1:Person{name:{fp}}),(p2:Person{name:{tp}}),p=allshortestpaths((p1)-[*..10]-(p2)) "
                                    "return p",fp=fperson,tp=tperson);
    nodes_total = []
    rels_total = []
    #all_nodes_total = []
    paths = []
    cnt = 0
    for datai in data:
        nodes = datai['p'].nodes()
        rels = datai['p'].relationships()
        # print rel
        # print nodes
        # print rels
        this_path = []
        this_path_val = 0
        this_path_values = []
        for i in range(0, len(nodes)):
            #all_nodes_total.append(nodes[i]['name'])
            if nodes[i]['name'] not in nodes_total:
                nodes_total.append(nodes[i]['name'])
            if i < len(nodes) - 1:
                rels_total.append(
                    {"start_node": nodes[i]['name'], "end_node": nodes[i+1]['name'], "val": rels[i]['value']})
                this_path.append(
                    {"start_node": nodes[i]['name'], "end_node": nodes[i + 1]['name'], "val": rels[i]['value']})
                this_path_val += rels[i]['value']
                this_path_values.append(rels[i]['value'])
        paths.append({'path': this_path, 'val': np.sum(this_path_values)})
    paths.sort(cmp=f2)

    return HttpResponse(json.dumps([nodes_total,rels_total,paths]), content_type="application/json")

