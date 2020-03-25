import src.volunteer
import src.classroom


class Assign:

    # adds all partners to same team
    def assign_partners(volunteer):

    # Matches people in an input list ("group") to a classroom they can make. Group can be list of drivers, t_leaders,
    # or others. If group is t_leaders or others the list will be sorted from lowest to highest availability.
    # TODO: Tries to match person with partially filled classrooms first. If they can't make any partially filled
    #  classrooms, try to place them in an classroom with no volunteers (yet).
    def assign_group(group, classrooms):

    # boolean if volunteer can make a class
    def volunteer_can_make_class(volunteer, classroom):
        return volunteer.schedule[classroom.start_time_schedule_index] >= classroom.volunteer_time_needed
    

#  don't depend on Assign objects (there are none)
Assign.assign_partners = staticmethod(Assign.assign_partners)
Assign.assign_group = staticmethod(Assign.assign_group)
Assign.volunteer_can_make_class = staticmethod(Assign.volunteer_can_make_class)

