import src.volunteer
import src.classroom



class Assign:

    # adds all partners to same team
    # TODO

    def assign_partners(self, volunteer):
        return

    # Matches people in an input list ("subgroup") to a classroom they can make. Subgroup can be list of drivers, t_leaders,
    # or others. If group is t_leaders or others the list will be sorted from lowest to highest availability.
    # TODO: Tries to match person with partially filled classrooms first. If they can't make any partially filled
    #  classrooms, try to place them in an classroom with no volunteers (yet).
    def assign_group(self, subgroup, nonempty_classrooms, empty_classrooms):
        for volunteer in subgroup:
            classroom_idx = 0

            while classroom_idx <= nonempty_classrooms.size - 1 and volunteer.group_number == -1:
                if volunteer_can_make_class(volunteer, nonempty_classrooms[classroom_idx]):
                    nonempty_classrooms[classroom_idx].assign_volunteer(volunteer)
                else:
                    classroom_idx += 1

            classroom_idx = 0

            while classroom_idx <= empty_classrooms.size - 1 and volunteer.group_number == -1:
                if volunteer_can_make_class(volunteer, empty_classrooms[classroom_idx]):
                    empty_classrooms[classroom_idx].assign_volunteer(volunteer)
                    nonempty_classrooms.append(empty_classrooms[classroom_idx])
                    empty_classrooms.pop(classroom_idx)
                else:
                    classroom_idx += 1
        return

    # boolean if volunteer can make a class
    def volunteer_can_make_class(volunteer, classroom):
        return volunteer.schedule[classroom.start_time_schedule_index] >= classroom.volunteer_time_needed

    def return_classrooms_possible(volunteer):
        return volunteer.classrooms_possible

    def sort_by_availability(list):
        list.sort(key=return_classrooms_possible)
        return list


#  don't depend on Assign objects (there are none)
Assign.assign_partners = staticmethod(Assign.assign_partners)
Assign.assign_group = staticmethod(Assign.assign_group)
Assign.volunteer_can_make_class = staticmethod(Assign.volunteer_can_make_class)
Assign.return_classrooms_possible = staticmethod(Assign.return_classrooms_possible)
Assign.sort_by_availability = staticmethod(Assign.sort_by_availability)
