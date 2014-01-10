import xml.etree.ElementTree as et
import requests


url = "https://10.140.11.30/appliance/avtrans"
username = "admin"
password = "1"


def wrap(subelements):
    # <avtrans>
    avtrans = et.Element("avtrans")
    # <sid></sid>
    et.SubElement(avtrans, "sid")
    # <action>login</action>
    action = et.SubElement(avtrans, "action")
    action.text = "login"
    # <agents><src>wmi</src><dest>controller</dest></agents>
    agents = et.SubElement(avtrans, "agents")
    et.SubElement(agents, "src").text = "wmi"
    et.SubElement(agents, "dest").text = "controller"
    # wrap actual request
    avtrans.extend(subelements)
    # </avtrans>
    return avtrans


def post(url, tree):
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    xml = et.tostring(tree)
    print ">>> %s" % xml
    response = requests.post(url, data=xml, headers=headers, verify=False)
    print "<<< %s" % response.text
    return response.text


def login(url, username, password):
    # <payload>
    #   <section structure="login">
    #     <parameter id="username" structure="RWtext"><value>admin</value></parameter>
    #     <parameter id="password" structure="password"><value>1</value></parameter
    #   </section>
    # </payload>
    payload = et.Element("payload")
    payload_section = et.SubElement(payload, "section")
    payload_section.set("structure", "login")
    parameter_username = et.SubElement(payload_section, "parameter")
    parameter_username.set("id", "username")
    parameter_username.set("structure", "RWtext")
    et.SubElement(parameter_username, "value").text = username
    parameter_password = et.SubElement(payload_section, "parameter")
    parameter_password.set("id", "password")
    parameter_password.set("structure", "password")
    et.SubElement(parameter_password, "value").text = password

    post(url, wrap([payload]))

login(url, username, password)
