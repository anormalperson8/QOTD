import json
import os

path = os.path.dirname(os.path.abspath(__file__))


class Server:
    def __init__(self, server_id: int, question_channel: int, moderator_roles: list,
                 role_to_ping: int):
        self.serverID = server_id
        self.question_channel = question_channel
        self.moderator_roles = moderator_roles
        self.role_to_ping = role_to_ping


# Returns a list of Server objects
def get_servers():
    f = open(path + "/data/server.json", 'r')
    data = json.load(f)
    servers = []
    for server in data["server"]:
        servers.append(Server(server["id"], server["questionChannel"],
                              server["moderatorRoles"], server["RoleToPing"]))
    f.close()
    return servers


# Returns the index of the server in the list of servers
def search_for_server_id(servers: list, server_id: int):
    return [i for i in range(len(servers)) if servers[i].serverID == server_id][0]


# Returns the server object in the list of servers
def search_for_server(servers: list, server_id: int):
    return [i for i in servers if i.serverID == server_id][0]


# Returns true if the server exists. False otherwise.
def server_exists(servers: list, server_id: int):
    return len([i for i in servers if i.serverID == server_id]) == 1


def write(servers: list[Server]):
    w = open(path + "/data/server2.json", 'w')
    objs = []
    for server in servers:
        s = {
            "id": server.serverID,
            "questionChannel": server.question_channel,
            "moderatorRoles": server.moderator_roles,
            "RoleToPing": server.role_to_ping
            }
        objs.append(s)
    obj = {"server": objs}
    w.write(json.dumps(obj, indent=2))
    w.close()
    os.remove(path + "/data/server.json")
    os.rename(path + "/data/server2.json", path + "/data/server.json")


# Edits server info
def modify(server_id: int, stat: bool, question_channel: int = None, moderator_role: int = None,
           role_to_ping: int = None):
    servers = get_servers()
    done = False
    message = "Problem: Server was not found."
    for server in servers:
        if server.serverID == server_id:
            if question_channel is not None:
                if stat:
                    if question_channel != server.question_channel:
                        server.question_channel = question_channel
                        done = True
                        message = f"Questioning channel is set to channel with ID {question_channel}."
                    else:
                        message = f"Problem: This is already the questioning channel!"
                else:
                    server.announcementChannel = -1
                    done = True
                    message = f"Questioning channel is removed."
                break

            if moderator_role is not None:
                if stat and moderator_role not in server.moderator_roles:
                    server.moderator_roles.append(moderator_role)
                    done = True
                    message = f"Role with ID {moderator_role} is added to the list of permitted roles."
                elif stat:
                    message = (f"Problem: Role with ID {moderator_role} could not be added to the list of "
                               f"permitted roles.")
                elif not stat and moderator_role in server.moderator_roles:
                    server.moderator_roles.remove(moderator_role)
                    done = True
                    message = f"Role with ID {moderator_role} is removed from the list of permitted roles."
                elif not stat:
                    message = (f"Problem: Role with ID {moderator_role} could not be removed from the list of "
                               f"permitted roles.")
                break

            if role_to_ping is not None:
                if stat:
                    if role_to_ping != server.role_to_ping:
                        server.role_to_ping = role_to_ping
                        done = True
                        message = f"Role to ping is set to role with id {role_to_ping}."
                    else:
                        message = f"Problem: This is already the role to ping!."
                else:
                    server.role_to_ping = -1
                    done = True
                    message = f"Role to ping is removed."
                break

    write(servers)
    return done, message

