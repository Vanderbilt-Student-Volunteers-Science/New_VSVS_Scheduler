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

        # for all volunteers in group
        for idx in range(len(self.volunteers)):
            curr_volunteer = self.volunteers[idx].free_time
            for day in curr_volunteer:
                for time in curr_volunteer[day]:

                    # If it's the first partner (idx = 0), then just copy their schedule into partners_schedule
                    if idx == 0:
                        partners_schedule[day][time] = curr_volunteer[day][time]

                    # If not the first partner and the time is not in partners_schedule then just skip
                    elif time not in partners_schedule[day]:
                        pass

                    # If not the first partner and the time in partners_schedule, check if partners_schedule or
                    # curr_volunteer has less free time at the time. Keep the one with the least time.
                    elif curr_volunteer[day][time] < partners_schedule[day][time]:
                        partners_schedule[day][time] = curr_volunteer[day][time]

        return partners_schedule

    def __str__(self):
        text_output = ""
        for volunteer in self.volunteers:
            if volunteer == self.volunteers[-1]:
                text_output += str(volunteer)
            else:
                text_output += str(volunteer) + ", "
        return text_output
