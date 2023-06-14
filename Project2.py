import numpy as np
import csv
import pandas as pd


def calculate_distance(instance1, instance2):
    distance = 0.0
    for i in range(len(instance1)):
        distance += (float(instance1[i]) - float(instance2[i])) ** 2
    distance = distance ** 0.5
    return distance


def calculate_accuracy(dataset):
    num_instances = len(dataset)
    correct_predictions = 0

    for instance in dataset:
        check_instance = instance[1:]  # features of current instance
        true_label = instance[0]  # label of current instance

        distances = []  # store distances to other instances
        labels = []  # store labels of other instances

        for other_instance in dataset:
            if instance == other_instance:
                continue
            other_label = other_instance[0]
            other_features = other_instance[1:]
            distance = calculate_distance(check_instance, other_features)
            distances.append(distance)
            labels.append(other_label)

        nearest_neighbor_index = np.argmin(distances)  # index of nn
        predicted_label = labels[nearest_neighbor_index]  # label of nn

        if predicted_label == true_label:
            correct_predictions += 1

    accuracy = (correct_predictions / num_instances) * 100

    return accuracy


def forward_search(dataset):
    num_features = len(dataset[0]) - 1
    selected_features = []  # 存储已选择的特征
    best_accuracy = 0.0

    for _ in range(num_features):
        best_feature = None
        for feature in range(1, num_features + 1):
            if feature not in selected_features:
                selected_features.append(feature)
                accuracy = calculate_accuracy(dataset)
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_feature = feature
                selected_features.remove(feature)

        if best_feature is not None:
            selected_features.append(best_feature)
        else:
            break

    return selected_features, best_accuracy


def backward_search(dataset):
    num_features = len(dataset[0]) - 1
    selected_features = list(range(1, num_features + 1))  # 存储已选择的特征
    best_accuracy = calculate_accuracy(dataset)

    while len(selected_features) > 0:
        worst_feature = None
        for feature in selected_features:
            selected_features.remove(feature)
            accuracy = calculate_accuracy(dataset)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
            else:
                worst_feature = feature
            selected_features.append(feature)

        if worst_feature is not None:
            selected_features.remove(worst_feature)
        else:
            break

    return selected_features, best_accuracy

print("Welcome to Jiang Zhu and Xiang Qian's Feature Selection Algorithm." )
filePath = input("Type in the name of the file to test:")  # /Users/connor/Desktop/data_sets/CS170_small_Data__20.txt
with open(filePath, 'r') as file:
    lines = file.readlines()

data = []
for line in lines:
    line = line.strip()
    row = line.split()
    print(row)
    data.append(row)

print(data)

print("This dataset has " + str(len(data[0]) - 1) + " features (not including the class attribute, with " + str(
        len(data)) + " instances.")
accuracyInit = calculate_accuracy(data)
print("Running nearest neighbor with all " + str(
        len(data[0]) - 1) + " features, using \"leave one out\" evaluation, accuracy is " + str(accuracyInit * 100) + "%.\n")

choice = input()
if choice == '1':
    forward_selected_features, forward_accuracy = forward_search(data)
elif choice == '2':
    backward_selected_features, backward_accuracy = backward_search(data)

forward_selected_features, forward_accuracy = forward_search(data)
backward_selected_features, backward_accuracy = backward_search(data)
