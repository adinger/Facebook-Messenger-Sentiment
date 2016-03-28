from bs4 import BeautifulSoup, NavigableString

####### change "me" and "out_file" #########
me = "Angela Ding"
out_file = "email_matrix.csv"
############################################


html_file = open("messages.htm", 'r', encoding="utf8")
soup = BeautifulSoup(html_file, 'html.parser')


def get_all_contacts(soup, me):
    all_contacts = {}
    conversations = []
    for thread in soup.find_all("div", { "class" : "thread" }):
        outer = thread
        contacts = [element for element in outer if isinstance(element, NavigableString)]
        # output of above: ['Ranran Li, Angela Ding, Shanshan Tian, April Xu, Maggie An, Corly Leung']
        contacts = contacts[0].split(', ')
        # output now: ['Ranran Li', 'Angela Ding', 'Shanshan Tian', 'April Xu', 'Maggie An', 'Corly Leung']
        # get total number of messages/conversations this contact has appeared in
        contacts_copy = contacts

        for contact in contacts_copy:
            if contact == me or contact.find("@facebook.com") != -1:
                contacts.remove(contact)
            elif contact not in all_contacts.keys():
                all_contacts[contact] = 1
            else:
                all_contacts[contact] += 1
                #print(contact)

        conversations.append(contacts)

    return all_contacts, conversations


def initialize_matrix(contact_set):
    matrix = {} # a dict of dicts to represent a matrix
    for contact in contact_set.keys():
        row = {}
        for c2 in contact_set.keys():
            row[c2] = 0

        matrix[contact] = row
        print(contact+": ")
        print(matrix[contact])
    return matrix


def populate_matrix(matrix, contact_set, recipients):
    total = len(recipients)

    for c1 in range(total-1):
        r1 = recipients[c1]
        if r1.find("@facebook.com") != -1:
            continue
        for c2 in range(c1+1,total):
            r2 = recipients[c2]
            if r2.find("@facebook.com") != -1:
                continue
            contact1 = r1
            contact2 = r2
            print(contact1, contact2)
            try:
                matrix[contact1][contact2] += 1
                matrix[contact2][contact1] += 1
            except KeyError:
                pass

        try:
            matrix[r1][r1] = contact_set[r1] # set diagonal values
        except KeyError:
            pass


def export_to_csv(matrix, file):
    out_file = open(file, 'wb')
    whole_list = ""
    for row in matrix.keys():
        out_row = ""
        for col in matrix[row].values():
            out_row += str(col)+","
        print(out_row)
        out_row += "\n"
        whole_list += out_row
    out_file.write(whole_list.encode('utf-8'))


contact_set, conversations = get_all_contacts(soup, me)
matrix = initialize_matrix(contact_set)

for recipient_list in conversations:
    populate_matrix(matrix, contact_set, recipient_list)

export_to_csv(matrix, out_file)







