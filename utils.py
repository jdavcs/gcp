import json


def get_label_counts(json_file):
    label_counts = {}
    with open(json_file, 'r') as f:
        data = json.load(f)
        for labels in data.values():
            for label, _ in labels:
                count = label_counts.get(label, 0)
                label_counts[label] = count + 1

    temp = [] #for sorting only
    for label, count in label_counts.items():
        temp.append((int(count), label)) #must convert to int!!
    temp.sort(reverse=True) #sort by counts in descending order
    for count, label in temp:
        formatted = '{:>7} {}'.format(count, label)
        print(formatted)


#or just do the counts in the shell:
# py utils.py | sort | uniq -c | sort -r 
def get_labels(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        for labels in data.values():
            for label, _ in labels:
                print(label)


if __name__ == '__main__':
    get_label_counts('data/fi_labels.json')
    #get_labels('data/fi_labels.json')
