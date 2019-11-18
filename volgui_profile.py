# -*- coding: latin_1 -*-
import json


class Profile:
    """
    This class manage all stuffs related to volatility profile

    """

    def __init__(self):
        """
        The choosen profile key is 'choosen_profile'
        """
        self.profile = {} # content of the profile, ex: {'KPCR for CPU 0': 2190789632, 'Suggested Profile(s)': 'Win7SP1x86_23418, Win7SP0x86, Win7SP1x86_24000, Win7SP1x86', 'Image Type (Service Pack)': 0, 'Image local date and time': '2016

    def build_profile(self, imageinfo_result):
        """
        Build a profile of the current image dump

        :param imageinfo_result: the result of the imageinfo command
        :return: None
        """

        elt_level0 = json.loads(imageinfo_result)
        profile_fields = elt_level0['columns'][0:]
        profile_fields_values = elt_level0['rows'][0]
        index = 0
        for field in profile_fields:
            self.profile[field] = profile_fields_values[index]
            index += 1

        suggested_profile = self.profile['Suggested Profile(s)']
        suggested_profile_list = suggested_profile.split(",")
        self.profile['choosen_profile'] = suggested_profile_list[0]

    def __repr__(self):
        """
        called when we call repr buildin method or enter the object name on the python cmdline

        :return: the object string representation
        """

        return "Profile list : {} \n Choosen_profile : {}".format(self.profile)

    def __str__(self):
        """
        called when we print the object with print function or convert the object to string with str function

        :return: the string representation of the object
        """
        return "Profile list : {} \n Choosen_profile : {}".format(self.profile)

    # def __del__(self):
    # put here the message to log when one instance of this object is deleted
