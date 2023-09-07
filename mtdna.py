import json

rCRS_file = "rCRS.txt"
fname = ".txt"



# Importing rCRS into array
db = []
f_db = open(rCRS_file)

for l in f_db:
    l = list(l.strip())
    db += l

chromosome = 26


f = open(fname)

def scores(hap, tot):
    wrong = []
    correct = []
    not_found = []

    for mut in hap["mutations"]:
        if ("." not in mut):
            if ("!" not in mut):
                mut_pos = mut[0:-1]
                mut_allele = mut[-1]
            else:
                mut_pos = mut[0:-2]
                mut_allele = db[int(mut_pos) - 1]
            if mut_pos in tot:
                if tot[mut_pos] == mut_allele:
                    correct.append(mut)
                else:
                    wrong.append(mut)
            else:
                not_found.append(mut)
    
       
    return {"correct": correct, "wrong": wrong, "not_found": not_found}


def score(scrs):
    return len(scrs["correct"]) - len(scrs["wrong"]) - 0.0001 * len(scrs["not_found"])





total_mt = {}

for l in f:
    l = l.strip().split()
    if (int(l[1]) == chromosome):

        total_mt[l[2]] = l[3]

f = open("mutations.json", "r")

mutations = json.load(f)

f.close()


s = []
for haplogroup in mutations:
    scrs = scores(haplogroup, total_mt)
    s.append({"name": haplogroup["name"], "score": score(scrs), "info": scrs})
s.sort(key = lambda x: x["score"], reverse=True)


for i, prediction in enumerate(s[0:20]):
    name = prediction["name"]
    scr = prediction["score"]
    matched = prediction["info"]["correct"]
    wrong = prediction["info"]["wrong"]
    no_test = prediction["info"]["not_found"]


    print(f"({i+1}) {name}")
    print("="*10)
    print(f"Score: {scr}")
    print(f"Mutations Matched ({len(matched)}):")
    print(", ".join(matched))

    print(f"Mutations NOT Matched ({len(wrong)}):")
    print(", ".join(wrong))

    print(f"Mutations NOT Tested ({len(no_test)}):")
    print(", ".join(no_test))



    print("")


# def printScores()

