import infection
import model
import visualize

def read_input(filename):
    graph = model.Graph()
    method, args = None, ()
    with open(filename) as f:
        command = f.readline().strip().split()
        users = f.readline().strip().split()
        for name in users:
            graph.add_user(model.User(name))

        infection_user = graph.get_user(command[1])
        if command[0] == '1':
            method = infection.total_infect
            args = (infection_user, command[2])
        elif command[0] == '2':
            method = infection.limited_infect
            args = (infection_user, command[2], int(command[3]))
        else:
            raise ValueError('Infection Type not valid')

        for line in f.readlines():
            class_users = line.strip().split()
            teacher_name, student_names = class_users[0], class_users[1:]

            teacher = graph.get_user(teacher_name)
            students = [graph.get_user(name) for name in student_names]
            graph.set_classroom(teacher, students)
    return graph, method, args

if __name__ == '__main__':
    print 'Starting Program'

    graph, method, args = read_input('input.txt')
    visualize.classrooms(graph)
    visualize.teachers(graph)
    visualize.student(graph)

    visualize.user_versions(graph)
    method(graph, *args)
    visualize.user_versions(graph)