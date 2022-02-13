import json

f = open("Top_Tracks_Data.json", 'r')
json_data = json.load(f)
f.close()

lst = ['danceability', 'acousticness', 'energy', 'valence']

organized_dict = {}
a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]

for track in json_data:
    if track[lst[0]] > 0.5:
        if track[lst[1]] > 0.5:
            if track[lst[2]] > 0.5:
                if track[lst[3]] > 0.5:   
                    a.append(track)
                else:
                    b.append(track)
            else:
                if track[lst[3]] > 0.5:
                    c.append(track)
                else:
                    d.append(track)
        else:
            if track[lst[2]] > 0.5:
                if track[lst[3]] > 0.5:
                    e.append(track)
                else:
                    f.append(track)
            else:
                if track[lst[3]] > 0.5:
                    g.append(track)
                else:
                    h.append(track)
    else:
        if track[lst[1]] > 0.5:
            if track[lst[2]] > 0.5:
                if track[lst[3]] > 0.5:
                    i.append(track)
                else:
                    j.append(track)
            else:
                if track[lst[3]] > 0.5:
                    k.append(track)
                else:
                    l.append(track)
        else:
            if track[lst[2]] > 0.5:
                if track[lst[3]] > 0.5:
                    m.append(track)
                else:
                    n.append(track)
            else:
                if track[lst[3]] > 0.5:
                    o.append(track)
                else:
                    p.append(track)


with open("organized_data.json", "w") as outfile:
        json.dump(organized_dict, outfile)

tree = \
    ["Do you prefer some dance music?(Y/N)", 
        ["Do you prefer some accoustic music?(Y/N)", 
            ["Do you prefer some loud and energetic music?(Y/N)", 
                ["Do you prefer some happy and positive music?(Y/N)",
                    [a,None,None],[b,None,None]],
                ["Do you prefer some happy and positive music?(Y/N)",
                    [c,None,None],[d,None,None]]], 
            ["Do you prefer louder music? (Y/N)",
                ["Do you prefer some happy and positive music?(Y/N)",
                    [e,None,None],[f,None,None]],
                ["Do you prefer some happy and positive music?(Y/N)",
                    [g,None,None],[h,None,None]]]],
        ["Do you prefer some accoustic music?(Y/N)", 
            ["Do you prefer some loud and energetic music?(Y/N)",
                ["Do you prefer some happy and positive music?(Y/N)",
                    [i,None,None],[j,None,None]],
                ["Do you prefer some happy and positive music?(Y/N)",
                    [k,None,None],[l,None,None]]], 
            ["Do you prefer some loud and energetic music?(Y/N)",
                ["Do you prefer some happy and positive music?(Y/N)",
                    [m,None,None],[n,None,None]],
                ["Do you prefer some happy and positive music?(Y/N)",
                    [o,None,None],[p,None,None]]]]]

with open("tree.json", "w") as outfile:
        json.dump(tree, outfile)
