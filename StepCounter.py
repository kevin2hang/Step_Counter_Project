import math
import matplotlib.pyplot as plt


def get_acc_for_csv(name):
    lines = []
    path = "C:\\Users\kevin\StepCounterProject-Python\step_data\\"
    with open(path + name) as reader:
        lines = reader.readlines()
    acc_x = [float(line.split(',')[0]) for line in lines[1:]]
    acc_y = [float(line.split(',')[1]) for line in lines[1:]]
    acc_z = [float(line.split(',')[2]) for line in lines[1:]]

    acc_mag = [math.sqrt(acc_x[i] ** 2 + acc_y[i] ** 2 + acc_z[i] ** 2) for i in range(len(acc_x))]
    return acc_mag


def find_mean(data):
    sum = 0
    for i in range(len(data)):
        sum += data[i]
    mean = sum / len(data)
    return mean


def find_standard_deviation(data, mean):
    sum_of_squared_deviations = 0
    for i in range(len(data)):
        deviation = data[i] - mean
        sum_of_squared_deviations += deviation ** 2
    return math.sqrt(sum_of_squared_deviations / (len(data) - 1))


def find_minimums(acc_mag):
    min_indexes = []
    min_values = []
    for i in range(1, len(acc_mag) - 1):
        if (acc_mag[i] < acc_mag[i - 1] and acc_mag[i] < acc_mag[i + 1]):
            min_indexes.append(i)
            min_values.append(acc_mag[i])
    return min_indexes, min_values


def get_peaks(data):
    peaks_x = []
    for i in range(1, len(data) - 1):
        if (data[i] > data[i - 1] and data[i] > data[i + 1]):
            peaks_x.append(i)
    peaks_y = [data[index] for index in peaks_x]
    return peaks_x, peaks_y


def get_steps_2(
        acc_mag):  # uses relative avg difference for diff, uses relative mean + relative stand dev for max cutoff
    min_indexes, min_values = find_minimums(acc_mag)
    max_indexes, max_values = get_peaks(acc_mag)

    min_index_being_analyzed = 0

    step_index = []
    step_values = []
    k = 1
    z_score = 2.5
    for max_index_analyzed in range(0, len(max_indexes), 1):
        while max_values[max_index_analyzed] - min_values[
            min_index_being_analyzed] < k * get_avg_diff(min_values, max_values,
                                                         max_index_analyzed) and max_index_analyzed < len(
            max_indexes) - 1 and min_index_being_analyzed < len(min_indexes) - 1:
            if max_values[max_index_analyzed + 1] > max_values[max_index_analyzed]:
                max_index_analyzed += 1
            min_index_being_analyzed += 1
        if max_values[max_index_analyzed] - min_values[min_index_being_analyzed] > k * get_avg_diff(min_values,
                                                                                                    max_values,
                                                                                                    max_index_analyzed) and \
                max_values[
                    max_index_analyzed] > get_large_enough_cutoff(acc_mag, max_indexes, max_index_analyzed, z_score):
            step_index.append(max_indexes[max_index_analyzed])
            step_values.append(max_values[max_index_analyzed])

    return step_index, step_values


def get_avg_diff(mins, maxes, i):
    n = 30
    if n / 2 <= i < len(mins) - n / 2:
        return float((sum(maxes[i - int(n / 2):i + int(n / 2)]) - sum(mins[i - int(n / 2):i + int(n / 2)])) / n)
    elif i >= 0 and i < len(maxes) - n:
        return float((sum(maxes[i:i + n]) - sum(mins[i:i + n])) / n)
    elif i < len(maxes) and i >= (n - 1):
        return (sum(maxes[i - (n - 1):i + 1]) - sum(mins[i - (n - 1):i + 1])) / n


def get_large_enough_cutoff(data, list_to_get_index_for_data, index, z):
    index_to_use = list_to_get_index_for_data[index]
    n = 20
    if (n < index_to_use < len(data) - n):
        mean = find_mean(data[index_to_use - n:index_to_use + n])
        return mean + z * find_standard_deviation(data[index_to_use - n:index_to_use + n], mean)
    elif index_to_use >= 0 and len(data) > 2 * n:
        mean = find_mean(data[index_to_use:index_to_use + 2 * n])
        return mean + z * find_standard_deviation(data[index_to_use:index_to_use + 2 * n], mean)
    elif index_to_use < len(data) and index_to_use - 2 * n >= 0:
        mean = find_mean(data[index_to_use - 2 * n:index_to_use])
        return mean + z * find_standard_deviation(data[index_to_use - 2 * n:index_to_use], mean)


names = ["1-200-step-regular.csv", "4-100-step-running.csv", "10-500-step-regular.csv", "11-400-step-regular.csv"]


def plot_steps(name, plotR, plotC, n):
    actual_steps = int(name.split("-")[1])
    acc = get_acc_for_csv(name)
    steps_x, steps_y = get_steps_2(acc)
    plt.subplot(plotR, plotC, n)
    plt.plot(acc, 'b-')
    plt.plot(steps_x, steps_y, 'ro')
    plt.title(name[:name.find(".")])
    plt.text(2, 6, str(len(steps_x) * 2) + " counted steps\n" + "Percent Error: " + str(
        100 * (len(steps_x) * 2 - actual_steps) / actual_steps) + "%", color="white", fontsize=12,
             bbox=dict(facecolor='black', alpha=0.5))


for i in range(len(names)):
    plot_steps(names[i], 2, 2, i + 1)
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.6)
plt.show()
