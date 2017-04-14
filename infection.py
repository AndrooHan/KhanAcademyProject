import collections


def total_infect(graph, user, new_version):
    if not user:
        return
    print '========================'
    print 'INFECTING user '+user.name+" with no limit"
    infected_classrooms = set()
    to_infect_classrooms = collections.deque(list(user.teacher | user.enrolled))
    to_infect_users = {user}
    while to_infect_classrooms:
        target_class_ID = to_infect_classrooms.popleft()
        if target_class_ID in infected_classrooms:
            continue

        infected_classrooms.add(target_class_ID)
        to_infect_users |= graph.classmembers[target_class_ID]

        for user in graph.classmembers[target_class_ID]:
            user_classes = user.enrolled | user.teacher
            to_infect_classrooms.extend(
                list(user_classes.difference(infected_classrooms))
            )
    for user in to_infect_users:
        user.version = new_version
    print 'Classrooms infected '+ str(sorted(list(infected_classrooms)))
    print 'Users infected ' + str(sorted([user.name for user in to_infect_users]))
    print '========================'

def limited_infect(graph, user, new_version, limit):
    print '========================'
    print 'INFECTING user '+user.name + " with limit: "+str(limit)
    user_classes = user.teacher | user.enrolled

    closest_infected_classes = _limited_infect_help(graph, set(), user_classes, limit)
    target_users = _unique_users(graph, closest_infected_classes)
    for user in target_users:
        user.version = new_version
    print 'Classrooms infected ' + str(sorted(list(closest_infected_classes)))
    print 'Users infected ' + str(sorted([user.name for user in target_users]))
    print '========================'


def _limited_infect_help(graph, infected_classes, class_set, limit):
    closest_count = len(_unique_users(graph, infected_classes))
    if closest_count >= limit:
        return infected_classes

    closest_class_set = infected_classes
    for class_id in class_set:
        new_class_set = reduce(
            lambda x, user: x.union(user.teacher | user.enrolled), graph.classmembers[class_id], set()
        )

        new_class_set |= class_set
        new_class_set -= infected_classes
        new_class_set.remove(class_id)

        temp_infected_classes = _limited_infect_help(graph, infected_classes.union({class_id}), new_class_set, limit)
        temp_user_count = len(_unique_users(graph, temp_infected_classes))
        if abs(limit - temp_user_count) < abs(limit - closest_count):
            closest_count, closest_class_set = temp_user_count, temp_infected_classes

    return closest_class_set


def _unique_users(graph,classes):
    return reduce(
        lambda users, class_id: users.union(graph.classmembers[class_id]), classes, set()
    )

