from typing import List, Tuple, Any, Optional
from numpy import array, arange, cumsum #type: ignore

import matplotlib #type: ignore
#matplotlib.use('agg') #prevents a tKinter error

from matplotlib import pyplot #type: ignore
from matplotlib.legend import Legend, Rectangle #type: ignore
from matplotlib.figure import Figure #type: ignore
from matplotlib.axes._subplots import Axes #type: ignore

from hare.main import Hare

def visualize_toxicity_for_one_conversation(hare_obj : Hare, conversation_index : int =0) -> None:

    # Make sure the hare obj is up-to-date
    hare_obj.update_status_history_for_conversation(conversation_index)

    # Create the x and y data
    speakers : List[str] = list(hare_obj.conversations[conversation_index].all_speakers)
    y : List[List[float]] = [[] for speaker in speakers]

    for status in hare_obj.status_per_conversation[conversation_index]:
        for series, speaker in zip(y, speakers):

            try:
                series.append(status[speaker])
            except KeyError:
                series.append(0)

    try:
        x : array = arange(len(y[0]))
    except IndexError:
        return

    y_stack : array = cumsum(y, axis=0)

    # Create the figure, basic settings
    fig : Figure = pyplot.figure()
    ax1 : Axes = fig.add_subplot(111)
    ax1.set_xlim([0, len(x) - 1])
    ax1.set_title('Toxicity per player')
    ax1.set_xlabel('# of turns')
    ax1.set_ylabel('Toxicity')

    # Figure out the horizontal ticks (and font for vertical)
    TICK_FREQUENCY : int = 1
    x_ticks : List[int] = []
    x_tick_labels : List[int] = []

    for i in x:
        x_ticks.append(int(i))
        x_tick_labels.append(int(i + 1))

    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_tick_labels)

    # Draw the figure
    colors : List[Tuple[float, float, float]] = [(248 / 255, 118 / 255, 109 / 255), (205 / 255, 150 / 255, 0 / 255), (124 / 255, 174 / 255, 1 / 255),
              (0 / 255, 190 / 255, 103 / 255), (0 / 255, 191 / 255, 196 / 255), (0 / 255, 169 / 255, 1.0)]

    for i in range(len(y)):

        if i == 0:
            starting_point = 0
        else:
            starting_point = y_stack[i - 1, :]

        ax1.fill_between(x, starting_point, y_stack[i, :], color=colors[i], facecolor=colors[i])

    # Legend
    legend_color_items : List[Rectangle] = [Rectangle((0, 0), 1, 1, fc=color, edgecolor="white") for color in colors]
    legend : Legend = ax1.legend(legend_color_items, speakers, loc='upper left', prop={'size': 10})
    legend.get_frame().set_linewidth(0.5)

    pyplot.margins(y=0)
    pyplot.show(y)

def get_metric_during_conversations(hare_obj : Hare,metric_name : str) -> List[float]:

    hare_obj.update_all_status_histories()
    length_of_longest_conversation : int = max(len(conversation) for conversation in hare_obj.conversations)
    scores : List[float] = []

    for utterance_index in range(length_of_longest_conversation):
        method = getattr(hare_obj,'calculate_'+metric_name+'_at_utterance')
        scores.append(method(utterance_index))

    return scores

def visualize_accuracy_during_conversations(hares : List[Hare]):

    from matplotlib import pyplot

    pyplot.clf()

    accuracies : List[float]
    lines : List[Any] = []

    for hare_obj in hares:
        accuracies = get_metric_during_conversations(hare_obj,'accuracy')
        line = pyplot.plot(accuracies)
        lines.append(line[0])

    pyplot.ylabel('Accuracy')
    pyplot.ylim(0,1)
    pyplot.xlabel('# of turns')
    pyplot.legend(lines, [hare_obj.name for hare_obj in hares])

    pyplot.show()

    return

def visualize_auc_during_conversations(hares : List[Hare], save_with_filename : Optional[str] = None):

    from matplotlib import pyplot

    pyplot.clf()

    areas_under_the_curve : List[float]
    lines : List[Any] = []

    for hare_obj in hares:
        areas_under_the_curve = get_metric_during_conversations(hare_obj,'auc')
        line = pyplot.plot(areas_under_the_curve)
        lines.append(line[0])

    pyplot.ylabel('AUC')
    pyplot.ylim(0.5,1)
    pyplot.xlabel('# of turns')
    pyplot.legend(lines, [hare_obj.name for hare_obj in hares])

    if save_with_filename is not None:
        pyplot.savefig(save_with_filename)
    else:
        pyplot.show()

    return

def visualize_precision_during_conversations(hares : List[Hare], save_with_filename : Optional[str] = None):

    from matplotlib import pyplot

    pyplot.clf()

    precisions : List[float]
    lines : List[Any] = []

    for hare_obj in hares:
        precisions = get_metric_during_conversations(hare_obj, 'precision')
        line = pyplot.plot(precisions)
        lines.append(line[0])

    pyplot.ylabel('Precision')
    pyplot.ylim(0,1)
    pyplot.xlabel('# of turns')
    pyplot.legend(lines, [hare_obj.name for hare_obj in hares])

    if save_with_filename is not None:
        pyplot.savefig(save_with_filename)
    else:
        pyplot.show()

    return


def visualize_recall_during_conversations(hares : List[Hare], save_with_filename : Optional[str] = None):

    from matplotlib import pyplot

    pyplot.clf()

    recalls : List[float]
    lines : List[Any] = []

    for hare_obj in hares:
        recalls = get_metric_during_conversations(hare_obj, 'recall')
        line = pyplot.plot(recalls)
        lines.append(line[0])

    pyplot.ylabel('Recall')
    pyplot.ylim(0,1)
    pyplot.xlabel('# of turns')
    pyplot.legend(lines, [hare_obj.name for hare_obj in hares])

    if save_with_filename is not None:
        pyplot.savefig(save_with_filename)
    else:
        pyplot.show()

    return

def visualize_fscore_during_conversations(hares : List[Hare], save_with_filename : Optional[str] = None):

    from matplotlib import pyplot

    pyplot.clf()

    fscores : List[float]
    lines : List[Any] = []

    for hare_obj in hares:
        fscores = get_metric_during_conversations(hare_obj, 'fscore')
        line = pyplot.plot(fscores)
        lines.append(line[0])

    pyplot.ylabel('F1-score')
    pyplot.ylim(0,1)
    pyplot.xlabel('# of turns')
    pyplot.legend(lines, [hare_obj.name for hare_obj in hares])

    if save_with_filename is not None:
        pyplot.savefig(save_with_filename)
    else:
        pyplot.show()

    return

def visualize_retrospective_precision_and_recall(hares : List[Hare]):

    from matplotlib import pyplot

    THRESHOLDS : List[float] = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

    lines : List[Any] = []

    for hare_obj in hares:

        hare_obj.update_all_status_histories()
        precisions: List[float] = hare_obj.calculate_retrospective_precision(THRESHOLDS)
        recalls: List[float] = hare_obj.calculate_retrospective_recall(THRESHOLDS)

        line = pyplot.plot(recalls,precisions)
        lines.append(line[0])

    pyplot.ylabel('Precision')
    pyplot.ylim(0,1)
    pyplot.xlabel('Recall')
    pyplot.xlim(0,1)
    pyplot.legend(lines, [hare_obj.name for hare_obj in hares])

    pyplot.show()

def visualize_retrospective_roc_curve(hares : List[Hare]):

    from matplotlib import pyplot

    fpr : List[float]
    tpr : List[float]

    lines : List[Any] = []

    for hare_obj in hares:

        hare_obj.update_all_status_histories()
        fpr, tpr = hare_obj.calculate_retrospective_roc_curve()

        line = pyplot.plot(fpr,tpr)
        lines.append(line[0])

    pyplot.ylabel('False positive rate')
    pyplot.ylim(0,1)
    pyplot.xlabel('True positive rate')
    pyplot.xlim(0,1)
    pyplot.legend(lines, [hare_obj.name for hare_obj in hares])

    pyplot.show()