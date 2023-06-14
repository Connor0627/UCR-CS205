import numpy as np
from copy import deepcopy
import sys


def calculate_accuracy(dataset, selected_features):
    if not selected_features:
        selected_features = list(range(1, len(dataset[0])))
    num_instances = len(dataset)
    correct_predictions = 0

    for instance in dataset:
        minDistance = sys.maxsize
        index = 0
        for other_instance in dataset:
            if not instance == other_instance:
                distance = 0.0
                for i in selected_features:
                    distance += (float(instance[i]) - float(other_instance[i])) ** 2
                if distance < minDistance:
                    minDistance = distance
                    index = dataset.index(other_instance)

        if instance[0] == dataset[index][0]:
            correct_predictions += 1

    accuracy = (correct_predictions / num_instances) * 100

    return accuracy


def forward_search(dataset):
    selected_features = []
    best_subset = []
    best_result = 0.0

    for _ in range(len(dataset[0]) - 1):
        best_feature = None
        best_accuracy = 0.0
        for feature in range(1, len(dataset[0])):
            if feature not in selected_features:
                selected_features.append(feature)
                accuracy = calculate_accuracy(dataset, selected_features)
                print("Using feature(s){" + str(selected_features) + "} accuracy is " + str(
                    "{:.1f}".format(accuracy)) + "%")
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_feature = feature
                selected_features.remove(feature)
        selected_features.append(best_feature)
        if best_accuracy > best_result:
            best_result = best_accuracy
            best_subset = deepcopy(selected_features)
        else:
            print("(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
        print("Feature set " + str(selected_features) + " was best, accuracy is " + str(
            "{:.1f}".format(best_accuracy)) + "%\n")
    print("Finished! The best features subset is " + str(best_subset) + ", its accuracy is " + str(
        "{:.1f}".format(best_result)) + "%")


def backward_search(dataset):
    selected_features = list(range(1, len(dataset[0])))
    best_subset = []
    best_result = 0.0
    for _ in range(len(dataset[0]) - 1):
        best_feature = selected_features[0]
        best_accuracy = 0.0
        temp_features = deepcopy(selected_features)
        for feature in temp_features:
            selected_features.remove(feature)
            accuracy = calculate_accuracy(dataset, selected_features)
            print("Using feature(s){" + str(selected_features) + "} accuracy is " + str(
                "{:.1f}".format(accuracy)) + "%")
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_feature = feature
            selected_features.append(feature)
        selected_features.remove(best_feature)
        if best_accuracy > best_result:
            best_result = best_accuracy
            best_subset = deepcopy(selected_features)
        else:
            print("(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
        print("Feature set " + str(selected_features) + " was best, accuracy is " + str(
            "{:.1f}".format(best_accuracy)) + "%\n")
    print("Finished! The best features subset is " + str(best_subset) + ", its accuracy is " + str(
        "{:.1f}".format(best_result)) + "%")


print("Welcome to Jiang Zhu and Xiang Qian's Feature Selection Algorithm.")
filePath = input("Type in the name of the file to test:")
# filePath = "/Users/connor/Desktop/data_sets/CS170_small_Data__33.txt"

with open(filePath, 'r') as file:
    lines = file.readlines()

data = []
for line in lines:
    line = line.strip()
    row = line.split()
    data.append(row)

print("This dataset has " + str(len(data[0]) - 1) + " features (not including the class attribute, with " + str(
    len(data)) + " instances.")
accuracyInit = calculate_accuracy(data, [])
print("Running nearest neighbor with all " + str(
    len(data[0]) - 1) + " features, using \"leave one out\" evaluation, we get an accuracy of " + str(
    "{:.1f}".format(accuracyInit)) + "%.\n")

print("Type the number of the algorithm you want to run.")
print("(1) Forward Selection.       (2) Backward Elimination")
choice = input()
print("Beginning search.")
if choice == '1':
    forward_search(data)
elif choice == '2':
    backward_search(data)