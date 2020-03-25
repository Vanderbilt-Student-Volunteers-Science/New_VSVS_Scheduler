import src.volunteer
import src.classroom


class Assign:

    # adds all partners to same team
    def assign_partners(volunteer):
        return

    
    # Matches people in an input list ("group") to a classroom they can make. Group can be list of drivers, t_leaders,
    # or others. If group is t_leaders or others the list will be sorted from lowest to highest availability.
    # TODO: Tries to match person with partially filled classrooms first. If they can't make any partially filled
    #  classrooms, try to place them in an classroom with no volunteers (yet).
    def assign_group(group, classrooms):
        return


    # helper function for sort_by_availability
    def merge(half_1, half_2):
        output = []
        index_1 = 0
        index_2 = 0

        while (index_1 < half_1.len() and index_2 < half_2.len()):
            if half_1[index_1].classrooms_possible < half_2[index_2].classrooms_possible:
                output.append(half_1[index_1])
                index_1 += 1
            else:
                output.append(half_2[index_2])
                index_2 += 1

        if index_1 == half_1.len():
            while index_2 < half_2.len():
                output.append(half_2[index_2])
                index_2 += 1
        else:
            while index_1 < half_1.len():
                output.append(half_1[index_1])
                index_1 += 1

        return output


    # merge sorts a list of volunteers by the number of classrooms they can make
    def sort_by_availability(list):
        if list.len() <= 1:
            return list
        pivot_idx = int(list.len() / 2)
        half_1 = sort_by_availability(list[0:pivot_idx])
        half_2 = sort_by_availability(list[pivot_idx:(list.len())])
        return merge(half_1, half_2)


    # boolean if volunteer can make a class
    def volunteer_can_make_class(volunteer, classroom):
        return volunteer.schedule[classroom.start_time_schedule_index] >= classroom.volunteer_time_needed


#  don't depend on Assign objects (there are none)
Assign.assign_partners = staticmethod(Assign.assign_partners)
Assign.assign_group = staticmethod(Assign.assign_group)
Assign.merge = staticmethod(Assign.merge)
Assign.sort_by_availability = staticmethod(Assign.sort_by_availability)
Assign.volunteer_can_make_class = staticmethod(Assign.volunteer_can_make_class)

