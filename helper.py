def make_is_target_file(option):
    def is_target_file(full_file_name):
        full_file_name_token = full_file_name.split("/")[-1].split("_")
        try:
            uid = int(full_file_name_token[0])
            date = int(full_file_name_token[1])
            tab = full_file_name_token[2]
            tab_chk = []
            for ind, chk in enumerate(option["tab"]):
                if chk == 1:
                    tab_chk.append(ind)

            is_target_uid = (option["uid"]["min"] <= uid) and ((uid <= option["uid"]["max"]) or option["uid"]["max"] == 0)
            is_target_date = (option["date"]["min"] <= date) and (
                        (date <= option["date"]["max"]) or option["date"]["max"] == 0)
            is_target_tab = int(tab) in tab_chk
            return is_target_uid and is_target_date and is_target_tab
        except ValueError:
            return False
    return is_target_file


def get_uid(full_file_name):
    return int(full_file_name.split('/')[-1].split('_')[0])
