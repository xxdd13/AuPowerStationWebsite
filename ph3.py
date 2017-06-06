#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 13:05:44 2017

@author: xinding
"""
from random import randint
import pandas as pd
import numpy as np
import csv
from collections import defaultdict
from flask import Flask, session, render_template, url_for, request, redirect
import json
import os

import seaborn as sns
import matplotlib.pyplot as plt
from numpy import arange




app = Flask(__name__, static_folder='.', static_url_path='')
SECRET_KEY=os.urandom(24)
app.config['SECRET_KEY']=os.urandom(24)
numheader=['GENERATIONMW','GENERATORNUMBER','PLANIMETRICACCURACY','SPATIALACCURACY']
indexdict={'OBJECTID':0,
               'FEATURETYPE':1,	
               'NAME':2,	
               'CLASS':3,
               'OPERATOR':	4,
               'OWNER':5,
               'SITEADDRESS':	6,
               'SITESUBURB':7,	
               'POSTCODE':	8,
               'STATE':9,
               'STATUS	':10,
               'GENERATIONTYPE':11,
               'PRIMARYFUELTYPE':	12,
               'PRIMARYSUBFUELTYPE':13,	
               'GENERATIONMW':	14,
               'GENERATORNUMBER':	15,
               'FEATURERELIABILITY':	16,
               'FEATURESOURCE':17,	
               'ATTRIBUTERELIABILITY':18,	
               'ATTRIBUTESOURCE':19,
               'PLANIMETRICACCURACY':20,
               'SPATIALACCURACY':21,
               'METADATACOMMENT':22	,
               'METADATALINK1':23,	
               'RESTRICTIONS':	24,
               'REVISED':25,
               'ENO':26
    }

def createtablejs():
    csv_data=readcsv('row')
    with open('raw.js', 'w') as fp:
        fp.write('(function () { \n')
        fp.write('var columnDefs = [\n')
        for head in csv_data[0]:
            if head==csv_data[0][-1]:
                txt='{headerName: "'+head+'", filter: "text",  field: "'+head+'"}\n'
            else:
                txt='{headerName: "'+head+'", filter: "text", field: "'+head+'"},\n'
            fp.write(txt)
        txt1='''];'''
        fp.write(txt1)
        txt2='''      
var gridOptions = {
        columnDefs: columnDefs,
        rowSelection: 'multiple',
        enableColResize: true,
        enableSorting: true,
        enableFilter: true,
        enableRangeSelection: true,
        suppressRowClickSelection: true,
        rowHeight: 22,
        animateRows: true,
        onModelUpdated: modelUpdated,
        debug: true
    };

    var btBringGridBack;
    var btDestroyGrid;

    // wait for the document to be loaded, otherwise
    // ag-Grid will not find the div in the document.
    document.addEventListener("DOMContentLoaded", function () {
        btBringGridBack = document.querySelector('#btBringGridBack');
        btDestroyGrid = document.querySelector('#btDestroyGrid');

        // this example is also used in the website landing page, where
        // we don't display the buttons, so we check for the buttons existance
        if (btBringGridBack) {
            btBringGridBack.addEventListener('click', onBtBringGridBack);
            btDestroyGrid.addEventListener('click', onBtDestroyGrid);
        }

        addQuickFilterListener();
        onBtBringGridBack();
    });

    function onBtBringGridBack() {
        var eGridDiv = document.querySelector('#bestHtml5Grid');
        new agGrid.Grid(eGridDiv, gridOptions);
        if (btBringGridBack) {
            btBringGridBack.disabled = true;
            btDestroyGrid.disabled = false;
        }
        gridOptions.api.setRowData(createRowData());
    }

    function onBtDestroyGrid() {
        btBringGridBack.disabled = false;
        btDestroyGrid.disabled = true;
        gridOptions.api.destroy();
    }

    function addQuickFilterListener() {
        var eInput = document.querySelector('#quickFilterInput');
        eInput.addEventListener("input", function () {
            var text = eInput.value;
            gridOptions.api.setQuickFilter(text);
        });
    }

    function modelUpdated() {
        var model = gridOptions.api.getModel();
        var totalRows = model.getTopLevelNodes().length;
        var processedRows = model.getRowCount();
        var eSpan = document.querySelector('#rowCount');
        eSpan.innerHTML = processedRows.toLocaleString() + ' / ' + totalRows.toLocaleString();
    }
    function createRowData() {
        var rowData = ROW_DATA;

        return rowData;
    }


var ROW_DATA = [\n    

\n'''
        fp.write(txt2)
        
        for row in csv_data[1::]:
            fp.write('{')
            for head in csv_data[0]:
                if head != 'METADATALINK1':
                    
                    if head==csv_data[0][-1]:
                        txt3='''"'''+head+'''":"'''+str(row[csv_data[0].index(head)])+'''"\n'''
                    else:
                        txt3='''"'''+head+'''":"'''+str(row[csv_data[0].index(head)])+'''",\n'''
                fp.write(txt3)
                
            fp.seek(-1, os.SEEK_END)
            fp.truncate()
            
            fp.write('},\n')
        fp.write('];\n')
        #fp.write('')
        
        fp.write('})();')

        
        
    return None


def random_col():
    st = 10**(6-1)
    ed = (10**6)-1
    return '#'+str(randint(st, ed))


def fixcsv():
    #open file and use csv reader to extract data into rows
    with open('NationalMajorPowerStations.csv', 'rb') as csvfile:
        rows = list(csv.reader(csvfile))
        for row in rows[1::]:
            row[9]=fixtypo(row[9]).title()
        with open('fixed.csv', 'w') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(rows)
def readcsv(mode):
    #open file and use csv reader to extract data into rows
    #with open('NationalMajorPowerStations.csv', 'rb') as csvfile:
    with open('fixed.csv', 'rb') as csvfile:
        rows = list(csv.reader(csvfile))
        
        if mode =='row':
            return rows
        elif mode == 'coln':
            return zip(*rows)
def createtally(lst):
    tally={}
    for l in lst:
        tally[l]=0
    return tally
        
def sorttally(tally):
    newlist=[]
    for key, val in sorted(tally.items()):
        
        newlist.append(val)
    return newlist

def fixtypo(word):
    typodict={'Western Austrlaia':'Western Australia'}
    try:
        return typodict[word].upper()
    except KeyError:
        return word.upper()
def state2abbrev(lst):
    new_lst=[]
    abbrev={'WESTERN AUSTRALIA':'AU-WA',
            'NEW SOUTH WALES':'AU-NSW',
            'QUEENSLAND':'AU-QLD',
            'VICTORIA':'AU-VIC',
            'TASMANIA':'AU-TAS',
            'SOUTH AUSTRALIA':'AU-SA',
            'NORTHERN TERRITORY':'AU-NT',
            'AUSTRALIAN CAPITAL TERRITORY':'AU-ACT'}
    for l in lst:
        newstate=abbrev[l[0]]
        new_lst.append([newstate,l[1]])
    return new_lst
        


@app.route('/')
def root():
    template = 'index.html'
    return render_template(template)
@app.route('/createjs')
def createjs():
    createtablejs()

    return root()
     
@app.route('/rawdata')
def rawdata():
    csv_data = readcsv('row')
    csv_header = csv_data[0]
    csv_body = csv_data[1::]
    
    template = 'rawdata.html'
    
    return render_template(template,
                           table_header=csv_header,
                           table_body=csv_body,
                           num_row=len(csv_body),
                           num_entity=len(csv_header))

@app.route('/member')
def member():
    template = 'member.html'
    return render_template(template)


    
@app.route('/poweroutput')
def poweroutput():
    template = 'poweroutput.html'
    select= request.args.get('select')
    if not select:
        select = 'STATE'
    #generation by state
    
    csv_data = readcsv('row')[1::]
    tally=defaultdict(float)
    for row in csv_data:
        val=row[indexdict['GENERATIONMW']]
        try:
            val=float(val)
        except ValueError:
            val=0
        key=fixtypo(row[indexdict[select]]).title()
        if key and not 'Null' in key:
            tally[key]+=val
    state_mw= list(tally.items())
    return render_template(template,
                               state_list=state_mw
                               )
    
@app.route('/testpivot',methods=['GET','POST'])
def testpivot(): 
    
    template = 'testpivot.html'
    
    csvfile = open('fixed.csv', 'r')
    jsonfile = open('mps2.json', 'w')
    fieldnames =list(readcsv('row')[0])
    print(fieldnames)
    reader = csv.DictReader(csvfile, fieldnames)
    data = json.dumps([r for r in reader])
    jsonfile.write(data) 
    
    return render_template(template)
    
    
    
    
@app.route('/builder',methods=['GET'])
def builder():  
    allowed=['PRIMARYFUELTYPE','PRIMARYSUBFUELTYPE','CLASS','OWNER','OPERATOR','STATE','STATUS','GENERATIONTYPE','GENERATORNUMBER','SPATIALACCURACY','PLANIMETRICACCURACY','REVISED']
    strallowed=[]
    for alld in allowed:
        strallowed.append([alld,alld.title()])
    mode=request.args.get('mode')
    if not mode :
        pivotidx = 'count'
        
    #fixcsv()
    template = 'builder.html'
    csv_data = readcsv('coln')
    header=[n[0] for n in csv_data]
    pivotidx=request.args.get('pivotidx')
    if not pivotidx or len(pivotidx)<1 or pivotidx=='row':
        pivotidx = 'STATE'
    cols=request.args.get('columns')
    if not cols or len(cols)<1 or cols=='col':
        cols = 'GENERATIONTYPE'
    val=request.args.get('v') 
    if not val:
        #val = 'all'
        val = 'GENERATIONMW'  
    print val,pivotidx,cols
    df=pd.read_csv('fixed.csv')
    
    #df=pd.pivot_table(df,index=["CLASS"],values=[val])
    #df=pd.pivot_table(df,index=["GENERATIONTYPE"],columns=[str('PRIMARYFUELTYPE')],values=["GENERATIONMW"],fill_value=0)
    
    if mode=="count":
        df=pd.pivot_table(df,index=[pivotidx],columns=[cols], values=[val],fill_value=0,aggfunc=lambda x: len(x.unique()))
    elif mode=='summ':
        df=pd.pivot_table(df,index=[pivotidx],columns=[cols],values=[val],dropna=True,aggfunc=[np.sum],fill_value=0)

    else:
        df=pd.pivot_table(df,index=[pivotidx],columns=[cols],values=[val],dropna=True,aggfunc=[np.mean],fill_value=0)


    valst=numheader
    cvalnum=99
    for index, row in df.iterrows():
        cvalnum=len(row)
    
    colnum=[2]
    while cvalnum>1:
        colnum.append(colnum[-1]+1)
        cvalnum-=1
    pandapivot=df.to_html(classes="table table-hover table-striped").replace('border="1"','border="0"').replace('-striped"','-striped" id="js-datatable" ')
    
    return render_template(template,header=strallowed,pandapivot=pandapivot,valst=valst,colnum=colnum)
    
@app.route('/geo')
def geo():
    viewmode= request.args.get('viewmode')
    template = 'geo.html'
    csv_data = readcsv('coln')
    if viewmode =='state':
        state_data=csv_data[9][1::]
        state_tally=defaultdict(int)
        for state in state_data:
            if state:
                state_tally[fixtypo(state)]+=1
        state_list=[]

        for key, val in state_tally.items():
            state_list.append([key,val])
        state_list.sort(key=lambda x: -x[1])
        yaxis=[]
        landarea=[2529875,1730648,1349129,983482,800642,227416,68401,2358]
        landlabel=['Western Australia','Queensland','Northern Territory','South Australia','New South Wales','Victoria','Tasmania','Australian Capital Territory']
        landdict={'WESTERN AUSTRALIA':2529875,
                 'QUEENSLAND':1730648,
                 'NORTHERN TERRITORY':1349129,
                 'SOUTH AUSTRALIA':983482,
                 'NEW SOUTH WALES':800642,
                 'VICTORIA':227416,
                 'TASMANIA':68401,
                 'AUSTRALIAN CAPITAL TERRITORY':2358      
                }
        for state in landlabel:
            for key, val in state_tally.items():
                if key.lower()==state.lower():
                    yaxis.append(val)
        lst=[]
        for n in state_list:
            lst.append([landdict[n[0]],n[1],n[0]])



        return render_template(template,
                               locationlist=state2abbrev(state_list),
                               locationtable=state_list,
                               control_var='state',
                               state_img=1,
                               lst=lst
                               )
    else:    
        loc_data=csv_data[7][1::]
        num_ps=0
        tally=defaultdict(int)
        for loc in loc_data:
            tally[loc]+=1
            num_ps+=1
        loc_list=[]
        loc_table=[]
        for key, val in tally.items():
            if key:
                loc_list.append([key,val])
                loc_table.append([key,val])  
            #else:
            #loc_table.append(["Unknown",val])
        loc_table.sort(key=lambda x: -x[1])
        loc_list.sort(key=lambda x: -x[1])
        return render_template(template,
                                       locationlist=loc_list,
                                       locationtable=loc_table,
                                       num_station=num_ps,
                                       control_var='regions')
    

@app.route('/ob')
def ob():
    template = 'ob.html'
    csv_data = readcsv('row')
    
    stlst = sorted(set(readcsv('coln')[indexdict['STATE']][1::]))
    
    xaxis=sorted(set(readcsv('coln')[indexdict['GENERATIONTYPE']][1::]))[2::]

    result=[]
    
    for x in xaxis:
        
        typedict={}
        
        for t in stlst:
            typedict[t]=0
        

        for row in csv_data[1::]:
            try:
                sub=float(row[indexdict['GENERATIONMW']])
            except ValueError:
                sub=0
            if row[indexdict['GENERATIONTYPE']]==x :
                typedict[row[indexdict['STATE']]]+=float(sub)
                
        d=[]
        
        for n in sorted(typedict.items()):
            
            d.append(n[1])
        
        result.append([x,d])
        
    #fuel 
    
    prifuel = sorted(readcsv('coln')[indexdict['PRIMARYFUELTYPE']][1::])
    prifueltally=defaultdict(int)
    sumprifuel=0
    for fuel in prifuel:
        prifueltally[fuel]+=1
        sumprifuel+=1
    prifuel_data=[]

    for key,val in prifueltally.items():
        prifuel_data.append([key,str(float(val)/float(sumprifuel)*100)[0:5]])
        
    #fuel 2
    select= 'PRIMARYFUELTYPE'
    
    tally=defaultdict(float)
    for row in csv_data[1::]:
        val=row[indexdict['GENERATIONMW']]
        try:
            val=float(val)
        except ValueError:
            val=0
        key=fixtypo(row[indexdict[select]]).title()
        if key and not 'Null' in key:
            tally[key]+=val
    state_mw= list(tally.items())
    
    
    #renew
    shownum=10
    
    ownerlist = sorted(set(readcsv('coln')[indexdict['OWNER']][1::]))
    renewtally=createtally(ownerlist)
    alltally=createtally(ownerlist)
    nontally=createtally(ownerlist)
    for owner in ownerlist:
        for row in csv_data:
            if row[indexdict['OWNER']]==owner:
                try:
                    sub=float(row[indexdict['GENERATIONMW']])
                except ValueError:
                    sub=0
                alltally[owner]+=sub
                if 'non' in row[indexdict['CLASS']].lower():
                    nontally[owner]+=sub
                elif row[indexdict['CLASS']].lower()=='renewable':
                    renewtally[owner]+=sub
                    
    renon=[]
    for owner,mw in alltally.items():
        renon.append([owner,mw,renewtally[owner],nontally[owner]])
    renon.sort(key=lambda lst: lst[1],reverse=True)
    renon=renon[0:shownum]
    
    #renewtally=sorttally(renewtally)
    #nontally=sorttally(nontally)
    
    renewtally=[]
    nontally=[]
    ownerlist=[]
    
    for r in renon:
        ownerlist.append(r[0])
        renewtally.append(r[2])
        nontally.append(r[3])  
    
    return render_template(template,dataset=result,xaxis=xaxis,stlst=stlst,fuelst=prifuel_data,
                           ownerlist=ownerlist,renewtally=renewtally,nontally=nontally,
                           state_list=state_mw)

    #return html % str(result)

if __name__ == "__main__":
    app.run(debug=True)
