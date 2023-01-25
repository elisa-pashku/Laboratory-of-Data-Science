import csv

def main():
    with open('./files/answerdatacorrect.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

        organization_dictionary = prepare_organization_data(data)
        geo_dictionary = prepare_geo_data(data)
        is_correct_dictionary = is_correct_answer(data)
        subject_dictionary = prepare_subject_data(data)
        date_dictionary = prepare_dates(data)
        prepare_user_data(data, geo_dictionary)
        prepare_answer_data(data, organization_dictionary, subject_dictionary, is_correct_dictionary)

# Organization table
def prepare_organization_data(data):
    organization_dictionary = {}
    current_index = 1   #Start from first row to skip the header

    for i, row in enumerate(data):
        #Skipping the header
        if i == 0:
            continue

        # Get GroupId, QuizId, SchemeOfWorkId
        org_tuple = (row[10], row[11], row[12])

        if organization_dictionary.get(org_tuple) is None:
            organization_dictionary[org_tuple] = current_index
            current_index += 1

    # Write in the new table
    org_table = open('./results/organizations.csv', 'w')
    org_writer = csv.writer(org_table)

    # Create header
    org_header = ['organizationid', 'groupid', 'quizid', 'schemeofworkid']
    org_writer.writerow(org_header)

    for key in organization_dictionary:
        row = [organization_dictionary[key]]
        row.extend(list(key))
        org_writer.writerow(row)

    org_table.close()

    return organization_dictionary

# Geography table
def prepare_geo_data(data):
    country_code_continent_dictionary = {}

    # Dataset used for getting the continents
    with open('./files/countries.csv', newline='') as f:
        reader = csv.reader(f)
        country_code_continent_data = list(reader)

        for i, row in enumerate(country_code_continent_data):
            if i == 0:
                continue
            country_code = row[1].lower()   # converting to lower case "alpha-2"

            if country_code == 'gb':        # uk not supported in the provided countries dataset
                country_code = 'uk'
            country_code_continent_dictionary[country_code] = [row[0], row[5]]  # get name of country & region(for the continent)

    geo_dictionary = {}
    current_index = 1
    for i, row in enumerate(data):

        if i == 0:
            continue
        # Using only Region and CountryCode
        geo_tuple = (row[15], row[16])

        if geo_dictionary.get(geo_tuple) is None:
            geo_dictionary[geo_tuple] = current_index
            current_index += 1

    geo_table = open('./results/geo.csv', 'w')
    geo_writer = csv.writer(geo_table)

    # Create header
    org_header = ['geoid', 'region', 'country_name', 'continent']
    geo_writer.writerow(org_header)

    for key in geo_dictionary:
        key_list = list(key)
        row = [geo_dictionary[key], key_list[0]]
        row.extend(country_code_continent_dictionary.get(key_list[1]))
        geo_writer.writerow(row)

    geo_table.close()

    return geo_dictionary



# The is_correct attribute is the main measure of the datawarehouse.
# You can compute its values by comparing the variables answer value and correct answer
def is_correct_answer(data):
    is_correct_dictionary = {}

    for i, row in enumerate(data):

        if i == 0:
            continue

        is_correct_dictionary[row[2]] = "Incorrect"

        # Compare CorrectAnswer with AnswerValue. If they are equal, the answer is correct => True.
        if row[3] == row[4]:
            is_correct_dictionary[row[2]] = "Correct"

    return is_correct_dictionary


# Create Subjects table
def prepare_subject_data(data):
    subject_metadata_dictionary = {}

    with open('./files/subject_metadata.csv', newline='') as f:
        reader = csv.reader(f)
        subject_metadata = list(reader)

        for i, row in enumerate(subject_metadata):
            if i == 0:
                continue

            # Get Name of Subject and Level
            subject_metadata_dictionary[row[0]] = (row[1], row[3])

    subject_dictionary = {}
    current_index = 1

    for i, row in enumerate(data):

        if i == 0:
            continue

        subject = row[13]    #Accessing SubjectId

        if subject_dictionary.get(subject) is None:
            subject_dictionary[subject] = current_index
            current_index += 1

    subject_table = open('./results/subject.csv', 'w')
    subject_writer = csv.writer(subject_table)

    subject_header = ['subjectid', 'description']
    subject_writer.writerow(subject_header)

    for key in subject_dictionary:
        row = [subject_dictionary[key]]

        subject_list = []

        subject_ids = key.strip('][').split(', ')

        for j, sub in enumerate(subject_ids):
            subject_list.append(subject_metadata_dictionary.get(sub))

        sorted_list = sorted(
            subject_list,
            key=lambda t: t[1]
        )

        # Joining the description of subject
        description = ', '.join([''.join(list(text_tuple)[0]) for i, text_tuple in enumerate(sorted_list)])

        row.append(description)
        subject_writer.writerow(row)

    subject_table.close()

    return subject_dictionary


# Create Dates table
def prepare_dates(data):
    date_dictionary = {}
    current_index = 1
    for i, row in enumerate(data):

        if i == 0:
            continue

        date_of_birth = row[6]

        if date_dictionary.get(date_of_birth) is None:
            date_dictionary[date_of_birth] = current_index
            current_index += 1

        date_answered = row[8].split(' ')[0]    #Accessing the first element of the list which gets created after the split

        if date_dictionary.get(date_answered) is None:
            date_dictionary[date_answered] = current_index
            current_index += 1

    date_table = open('./results/dates.csv', 'w')
    date_writer = csv.writer(date_table)

    date_header = ['dateid', 'date', 'day', 'month', 'year', 'quarter']
    date_writer.writerow(date_header)

    for key in date_dictionary:
        dateid = key[:4]+key[5:7]+key[8:] #substring for the ID
        date = key
        split_date = key.split('-')
        day, month, year = split_date[2], split_date[1], split_date[0]  # get day, month, year from the date
        quarter = (int(month) + 2) // 3

        row = [dateid, date, day, month, year, quarter]

        date_writer.writerow(row)

    date_table.close()

    return date_dictionary

# Create Users table
def prepare_user_data(data, geo_dictionary):
    user_dictionary = {}

    for i, row in enumerate(data):

        if i == 0:
            continue

        userid = row[1]

        if user_dictionary.get(userid) is None:
            geo_tuple = (row[15], row[16])
            geoid = geo_dictionary[geo_tuple]

            dateofbirthid = row[6][:4]+row[6][5:7]+row[6][8:]

            # Decided that if gender=1 the student will be female (F), else student is male (M)
            genderid = int(row[5])
            if genderid == 1:
                genderid = 'F'
            else:
                genderid = 'M'

            user_dictionary[userid] = [userid, dateofbirthid, geoid, genderid]

    user_table = open('./results/users.csv', 'w')
    user_writer = csv.writer(user_table)

    user_header = ['userid', 'dateofbirthid', 'geoid', 'gender']
    user_writer.writerow(user_header)

    for key in user_dictionary:
        user_writer.writerow(user_dictionary[key])

    user_table.close()

    return user_dictionary

#Create Answers table
def prepare_answer_data(data, organization_dictionary, subject_dictionary, is_correct_dictionary):

    answer_table = open('./results/answers.csv', 'w')
    answer_writer = csv.writer(answer_table)

    answer_header = [
        'answerid',
        'questionid',
        'userid',
        'organizationid',
        'dateid',
        'subjectid',
        'answer_value',
        'correct_answer',
        'is_correct',
        'confidence'
    ]

    answer_writer.writerow(answer_header)

    for i, row in enumerate(data):

        if i == 0:
            continue

        org_tuple = (row[10], row[11], row[12])

        answerid = row[2]
        questionid = row[0]
        userid = row[1]
        organizationid = organization_dictionary[org_tuple]
        date_answered =row[8].split(' ')[0]
        dateid = date_answered[:4]+date_answered[5:7]+date_answered[8:]
        subjectid = subject_dictionary[row[13]]
        answer_value = row[4]
        correct_answer = row[3]
        is_correct = is_correct_dictionary[row[2]]
        confidence = row[9]

        values = [
            answerid,
            questionid,
            userid,
            organizationid,
            dateid,
            subjectid,
            answer_value,
            correct_answer,
            is_correct,
            confidence
        ]

        answer_writer.writerow(values)

    answer_table.close()


main()
