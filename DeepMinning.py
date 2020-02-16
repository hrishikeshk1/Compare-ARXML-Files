import xml.etree.cElementTree as treepackage

px = "{http://autosar.org/schema/r4.0}"

def digAllTags(ref, key_tag):
    """
    Return a list of all descendants of 'ref' tag that match key_tag

    Given a particular tag(ref) in an xml,
    this function recursively fetches each and every tag provided by the key_tag argument,
    that is a descendant of the tag defined by the ref argument and returns a list of all
    tags with their descendants.
    """
    G_ore = ref.findall(key_tag)
    for i in range(len(ref)):
        if(len(ref[i]) > 0):
            G_ore.extend(digAllTags(ref[i], key_tag))
    return G_ore

def getUniqueDescendant(ref, key_tag):
    """
    Return the one unique descendant tag of 'ref' tag that matches key_tag

    Given a particular tag(ref) in an xml,
    this function recursively fetches the one unique tag defined by key_tag that is the
    descendant of ref.
    In case the key_tag is not unique, that is, if there are more than one 'key_tag's that are descendants of ref,
    this function will throw an exception
    """
    G_ore = ref.findall(key_tag)
    for i in range(len(ref)):
        if (len(ref[i]) > 0):
            G_ore.extend(digAllTags(ref[i], key_tag))
    if len(G_ore) > 1:
        raise Exception(f'There are multiple instances of {key_tag} tag in {ref.tag} tag')
    elif len(G_ore) == 0:
        return -1
    return G_ore[0]

def getUniqueChild(ref, key_tag):
    """
    Return the one unique child tag of 'ref' tag that matches key_tag

    Given a particular tag(ref) in an xml,
    this function iteratively fetches the one unique tag defined by key_tag that is the
    direct child of ref.
    In case the key_tag is not unique, that is, if there are more than one 'key_tag's that are direct children of ref,
    this function will throw an exception
    """
    G_ore = []
    for i in range(len(ref)):
       if ref[i].tag == key_tag:
           G_ore.append(ref[i])
    if len(G_ore) > 1:
        raise Exception(f'There are multiple instances of {key_tag} tag in {ref.tag} tag')
    elif len(G_ore) == 0:
        return -1
    return G_ore[0]

