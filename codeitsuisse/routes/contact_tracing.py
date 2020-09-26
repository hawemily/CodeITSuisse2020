import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/contact_trace', methods=['POST'])
def evaluate_contact_tracing():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    infected = data['infected']
    origin = data['origin']
    cluster = data['cluster']
    result = contact_trace(origin, infected, cluster)
    logging.info("My result :{}".format(result))
    return result


# determine if mutation is silent or not, also return number of differences
def compare_gene(gene1, gene2):
    num_differences = 0
    is_first_char_change = False
    for i in range(len(gene1)):
        if gene1[i] != gene2[i]:
            if i == 0:
                is_first_char_change = True
            num_differences += 1
    return num_differences, is_first_char_change


def eval_mutation(infected, origin):
    infected_genome = infected['genome']
    infected_genome_list = infected_genome.split("-")
    origin_genome = origin['genome']
    origin_genome_list = origin_genome.split("-")
    num_of_first_char_edited = 0
    total_diff = 0
    is_non_silent = False
    for x in range(len(infected_genome_list)):
        (diff, first_char_change) = compare_gene(infected_genome_list[x], origin_genome_list[x])
        if first_char_change:
            num_of_first_char_edited += 1
        total_diff += diff

    if num_of_first_char_edited > 1:
        is_non_silent = True

    return is_non_silent, total_diff


def create_string(s, is_non_silent, origin, infected):
    s += infected['name']
    if is_non_silent:
        s += '*'
    s += ' -> '
    s += origin['name']
    return s


def find_closest_mutation(infected, cluster):
    smallestDiff = sys.maxsize
    is_non_silent = False
    smallestDiffCluster = {}
    for i in range(len(cluster)):
        (is_non_silent_mutation, diff) = eval_mutation(infected, cluster[i])
        if smallestDiff > diff:
            smallestDiff = diff
            is_non_silent = is_non_silent_mutation
            smallestDiffCluster = cluster[i]
        if diff == 0:
            break

    return smallestDiffCluster, is_non_silent, smallestDiff


def init_dict_of_closest_cluster(closest_cluster_btw_one_another, cluster):
    prev_cluster_elem = cluster[0]
    for i in range(len(cluster)):
        (clusterMutation, is_non_silent_cluster, smallestDiff) = find_closest_mutation(prev_cluster_elem,
                                                                                       cluster[i + 1:])
        closest_cluster_btw_one_another[cluster[i]["name"]] = [clusterMutation['name'], is_non_silent_cluster]


def find_cluster_from_clusters(prev_closest_cluster, cluster):
    for i in range(len(cluster)):
        if cluster[i]["name"] == prev_closest_cluster:
            return cluster[i]


def contact_trace(origin, infected, cluster):
    trace_array = []
    s = ""
    (is_non_silent_origin, diff_infected_origin) = eval_mutation(infected, origin)
    if len(cluster) == 0:
        s = create_string(s, is_non_silent_origin, origin, infected)
        trace_array.append(s)
    else:
        (closestClusterToInfected, is_non_silent_cluster, smallestDiff) = find_closest_mutation(infected, cluster)
        closest_cluster_btw_one_another = {}
        if diff_infected_origin < smallestDiff:
            s = create_string(s, is_non_silent_origin, origin, infected)
            trace_array.append(s)
        elif diff_infected_origin == smallestDiff:
            s = create_string(s, is_non_silent_origin, origin, infected)
            trace_array.append(s)
            clusterStr = create_string(s, is_non_silent_cluster, closestClusterToInfected, infected)
            init_dict_of_closest_cluster(closest_cluster_btw_one_another, cluster)
            (next_closest_cluster_infection_name, non_silent) = closest_cluster_btw_one_another[
                closestClusterToInfected["name"]]
            while next_closest_cluster_infection_name is not None:
                if non_silent:
                    clusterStr += "*"
                clusterStr += " -> "
                clusterStr += next_closest_cluster_infection_name
                (next_closest_cluster_infection_name, non_silent) = closest_cluster_btw_one_another[
                    closestClusterToInfected[next_closest_cluster_infection_name]]
            trace_array.append(clusterStr)
        else:
            init_dict_of_closest_cluster(closest_cluster_btw_one_another, cluster)
            clusterStr = create_string(s, is_non_silent_cluster, closestClusterToInfected, infected)
            (next_closest_cluster_infection_name, non_silent) = closest_cluster_btw_one_another[
                closestClusterToInfected["name"]]
            prev_closest_cluster_name = next_closest_cluster_infection_name
            while next_closest_cluster_infection_name is not None:
                if non_silent:
                    clusterStr += "*"
                clusterStr += " -> "
                clusterStr += next_closest_cluster_infection_name
                prev_closest_cluster_name = next_closest_cluster_infection_name
                (next_closest_cluster_infection_name, non_silent) = closest_cluster_btw_one_another[
                    closestClusterToInfected[next_closest_cluster_infection_name]]
            prev_cluster = find_cluster_from_clusters(prev_closest_cluster_name)
            (_, non_silent) = eval_mutation(prev_cluster, origin)
            if non_silent:
                clusterStr += "*"
            clusterStr += " -> "
            clusterStr += origin["name"]

    return trace_array
