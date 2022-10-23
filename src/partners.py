class Partners:
    def __init__(self, volunteers_list: list):
        """

        :param volunteers_list:
        """
        self.volunteers = volunteers_list
        self.group_size = len(volunteers_list)
        self.free_time = self.create_partner_schedule()
        self.group_number = -1
        self.classrooms_possible = 0

    def create_partner_schedule(self):
        """

        :return:
        """
        partners_schedule = {"Monday": {}, "Tuesday": {}, "Wednesday": {}, "Thursday": {}}
        for i in range(len(self.volunteers)):  # for all volunteers in group
            curr_volunteer = self.volunteers[i].free_time
            for day in partners_schedule:  # for each weekday
                for time in curr_volunteer[day]:  # for each time
                    if i == 0:
                        partners_schedule[day][time] = curr_volunteer[day][time]
                    elif time not in partners_schedule[day]:
                        pass
                    elif curr_volunteer[day][time] < partners_schedule[day][time]:
                        partners_schedule[day][time] = curr_volunteer[day][time]
        return partners_schedule
