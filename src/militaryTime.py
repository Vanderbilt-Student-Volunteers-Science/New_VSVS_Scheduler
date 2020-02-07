class MilitaryTime:

    def convert_to_military(time):
        time_list = time.split(':', 2)
        time_list2 = time_list[1].split(' ', 2)  # split into minutes and AM/PM

        if time_list2[1] == 'AM':
            return (100 * time_list[0]) + time_list2[0]
        else:
            return 1200 + (100 * time_list[0]) + time_list2[0]


#  doesn't depend on a MilitaryTime object (there are none)
MilitaryTime.convert_to_military = staticmethod(MilitaryTime.convert_to_military)
