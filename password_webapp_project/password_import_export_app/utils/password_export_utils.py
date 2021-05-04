csv_fieldnames_list = ["description", "password", "expiration_date", "password_shared_users"]


def parse_password_to_csv_file(password_obj, csv_fieldnames):
    row_dict = {}
    for model_field_name in csv_fieldnames:
        val = getattr(password_obj, model_field_name, "-")
        if model_field_name == "password_shared_users":
            val = get_password_shared_users(password_obj)

        row_dict[model_field_name] = val
    return row_dict


def get_password_shared_users(password_obj):
    password_shared_users = [str(user) for user in password_obj.password_shared_users.all()]
    if len(password_shared_users):
        val = ",".join(password_shared_users)
        return val
    return "-"
