import json

f = open("Top_Tracks_Data.json", 'r')
json_data = json.load(f)
f.close()

lst = ['danceability', 'acousticness', 'energy', 'valence']

organized_dict = {}
a = organized_dict[f'high {lst[0]} high {lst[1]} high {lst[2]} high {lst[3]}'] = []
b = organized_dict[f'high {lst[0]} high {lst[1]} high {lst[2]} low {lst[3]}'] = []
c = organized_dict[f'high {lst[0]} high {lst[1]} low {lst[2]} high {lst[3]}'] = []
d = organized_dict[f'high {lst[0]} high {lst[1]} low {lst[2]} low {lst[3]}'] = []
e = organized_dict[f'high {lst[0]} low {lst[1]} high {lst[2]} high {lst[3]}'] = []
f = organized_dict[f'high {lst[0]} low {lst[1]} high {lst[2]} low {lst[3]}'] = []
g = organized_dict[f'high {lst[0]} low {lst[1]} low {lst[2]} high {lst[3]}'] = []
h = organized_dict[f'high {lst[0]} low {lst[1]} low {lst[2]} low {lst[3]}'] = []
i = organized_dict[f'low {lst[0]} high {lst[1]} high {lst[2]} high {lst[3]}'] = []
j = organized_dict[f'low {lst[0]} high {lst[1]} high {lst[2]} low {lst[3]}'] = []
k = organized_dict[f'low {lst[0]} high {lst[1]} low {lst[2]} high {lst[3]}'] = []
l = organized_dict[f'low {lst[0]} high {lst[1]} low {lst[2]} low {lst[3]}'] = []
m = organized_dict[f'low {lst[0]} low {lst[1]} high {lst[2]} high {lst[3]}'] = []
n = organized_dict[f'low {lst[0]} low {lst[1]} high {lst[2]} low {lst[3]}']=  []
o = organized_dict[f'low {lst[0]} low {lst[1]} low {lst[2]} high {lst[3]}'] = []
p = organized_dict[f'low {lst[0]} low {lst[1]} low {lst[2]} low {lst[3]}'] = []

for track in json_data:
    if track[lst[0]] > 0.5:
        if track[lst[1]] > 0.5:
            if track[lst[2]] > 0.5:
                if track[lst[3]] > 0.5:
                    organized_dict[f'high {lst[0]} high {lst[1]} high {lst[2]} high {lst[3]}'].append(track)
                else:
                    organized_dict[f'high {lst[0]} high {lst[1]} high {lst[2]} low {lst[3]}'].append(track)
            else:
                if track[lst[3]] > 0.5:
                    organized_dict[f'high {lst[0]} high {lst[1]} low {lst[2]} high {lst[3]}'].append(track)
                else:
                    organized_dict[f'high {lst[0]} high {lst[1]} low {lst[2]} low {lst[3]}'].append(track)
        else:
            if track[lst[2]] > 0.5:
                if track[lst[3]] > 0.5:
                    organized_dict[f'high {lst[0]} low {lst[1]} high {lst[2]} high {lst[3]}'].append(track)
                else:
                    organized_dict[f'high {lst[0]} low {lst[1]} high {lst[2]} low {lst[3]}'].append(track)
            else:
                if track[lst[3]] > 0.5:
                    organized_dict[f'high {lst[0]} low {lst[1]} low {lst[2]} high {lst[3]}'].append(track)
                else:
                    organized_dict[f'high {lst[0]} low {lst[1]} low {lst[2]} low {lst[3]}'].append(track)
    else:
        if track[lst[1]] > 0.5:
            if track[lst[2]] > 0.5:
                if track[lst[3]] > 0.5:
                    organized_dict[f'low {lst[0]} high {lst[1]} high {lst[2]} high {lst[3]}'].append(track)
                else:
                    organized_dict[f'low {lst[0]} high {lst[1]} high {lst[2]} low {lst[3]}'].append(track)
            else:
                if track[lst[3]] > 0.5:
                    organized_dict[f'low {lst[0]} high {lst[1]} low {lst[2]} high {lst[3]}'].append(track)
                else:
                    organized_dict[f'low {lst[0]} high {lst[1]} low {lst[2]} low {lst[3]}'].append(track)
        else:
            if track[lst[2]] > 0.5:
                if track[lst[3]] > 0.5:
                    organized_dict[f'low {lst[0]} low {lst[1]} high {lst[2]} high {lst[3]}'].append(track)
                else:
                    organized_dict[f'low {lst[0]} low {lst[1]} high {lst[2]} low {lst[3]}'].append(track)
            else:
                if track[lst[3]] > 0.5:
                    organized_dict[f'low {lst[0]} low {lst[1]} low {lst[2]} high {lst[3]}'].append(track)
                else:
                    organized_dict[f'low {lst[0]} low {lst[1]} low {lst[2]} low {lst[3]}'].append(track)


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

