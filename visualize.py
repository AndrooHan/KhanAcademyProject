def teachers(graph):
    print 'Teachers'
    users = sorted(graph.user_map.values())
    for user in users:
        print user.name+"("+str(user.version)+")" + " teaches classes: " + str(user.teacher)


def student(graph):
    print 'Students'
    users = sorted(graph.user_map.values())
    for user in users:
        print user.name+"("+str(user.version)+")" + " enrolled in classes: " + str(user.enrolled)


def classrooms(graph):
    print 'Classrooms'
    for key in sorted(graph.classmembers.keys()):
        print 'ID: '+key+" "+ str([user.name for user in graph.classmembers[key]])


def user_versions(graph):
    print 'User Versions'
    for user_name in sorted(graph.user_map.keys()):
        print user_name + ' : ' + graph.user_map[user_name].version