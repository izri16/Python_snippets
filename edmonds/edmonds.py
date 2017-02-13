import copy

# actions
P1 = 'P1'
P2 = 'P2'
P3 = 'P3'
P4 = 'P4'


class HungTree:

    def __init__(self, elements):
        self.root = elements[0]


class Flower:

    def __init__(self, flowers, stem, charge, color, vertex=None):
        self.flowers = flowers
        if (stem is None):
            self.stem = self
        else:
            self.stem = stem
        self.charge = charge
        self.edge_border = {}
        self.color = color
        self.is_outer = True
        self.outer = None
        # ID of related vertex. Consider only for blue flowers.
        self.vertex = vertex
        # Pointer to next blue flower. Consider only for blue flowers.
        self.next = []

    def get_next(self):
        '''
        Return next outer flowers to be iterated from current flower.
        Should be called only on outer nodes.
        '''
        if (not self.is_outer):
            raise Exception('Can not call get_next on non outer node')
        else:
            blue_flowers = self.get_all_blue_flowers()
            next_outer_flowers = []
            for b in blue_flowers.keys():
                for n in b.next:
                    if (n not in blue_flowers):
                        if (n.is_outer):
                            next_outer_flowers.append(n)
                        else:
                            next_outer_flowers.append(n.outer)
            return next_outer_flowers

    def get_all_blue_flowers(self):
        '''
        Retreive all blue flowers that occurs in current flower.
        '''
        blue_flowers = {}
        if (self.color == 'blue'):
            blue_flowers[self] = 1
            return blue_flowers

        stack = copy.copy(self.flowers)
        while(len(stack)):
            last = stack.pop()
            if (last.color == 'green'):
                stack += last.flowers
            if (last.color == 'blue'):
                blue_flowers[last] = 1
        return blue_flowers


def get_flower(blue_flowers, item):
    '''
    Retrieve blue flower based on vertex id.
    '''
    return blue_flowers[item]


def add_charge_to_tree(node, eps, position, visited):
    visited[node] = 1
    if (position[0] % 2 == 0):
        node.charge += eps
    else:
        node.charge += (eps * (-1))
    for n in node.get_next():
        if (n not in visited):
            add_charge_to_tree(n, eps, [position[0] + 1], visited)


def add_charge(flowers, vertex_barbels, min_e, hung_trees):
    # add charge to trees +1, -1
    for t in hung_trees:
        add_charge_to_tree(t.root, min_e, [0], {})


def get_outer_flower(node, vertex, visited):
    '''
    Get outer flower for given vertex value
    in given node(tree) if exists, otherwise return False.
    '''
    visited[node] = 1
    if (node.color == 'blue' and node.vertex == vertex):
        return node
    if (node.color == 'green'):
        stack = copy.copy(node.flowers)
        while(len(stack)):
            last = stack.pop()
            if (last.color == 'green'):
                stack += last.flowers
            if (last.color == 'blue' and last.vertex == vertex):
                return node
    for n in node.get_next():
        if (n not in visited):
            next_outer = n
            if (n.is_outer is False):
                next_outer = n.outer
            res = get_outer_flower(next_outer, vertex, visited)
            if (res):
                return res
    return False


def set_outer_flags(inner_flowers, f):
    '''
    When outer flower is created mark all descendants as not outer
    and add them reference to outer flower.
    '''
    for inner in inner_flowers:
        inner.is_outer = False
        inner.outer = f
        if (inner.flowers):
            set_outer_flags(inner.flowers, f)


def set_new_stems(node, stem):
    if (node.color == 'green'):
        node.stem = stem
        stack = copy.copy(node.flowers)
        while(len(stack)):
            last = stack.pop()
            if (last.color == 'green'):
                last.stem = stem
                stack += last.flowers


def get_edge_border_charge(f, u, v):
    has_u = False
    has_v = False
    stack = copy.copy(f.flowers)
    while(len(stack)):
        last = stack.pop()
        if (last.color == 'green'):
            stack += last.flowers
        elif (last.vertex == u):
            has_u = True
        elif (last.vertex == v):
            has_v = True
    if ((has_u and has_v) or (not has_u and not has_v)):
        return 0
    else:
        return f.charge


def is_even(node, tree_flower, level, visited):
    visited[node] = 1
    if (node is tree_flower):
        return (level % 2 == 0)
    for n in node.get_next():
        if (n not in visited):
            ret = is_even(n, tree_flower, level + 1, visited)
            if (ret is not None):
                return ret


def find_min_green(node, prev, previous, level, min_charge, bubble, visited):
    visited[node] = 1
    if (level % 2 == 1 and node.color == 'green'):
        if (node.charge < min_charge[0]):
            min_charge[0] = node.charge
            bubble[0] = node
            previous[0] = prev
    for n in node.get_next():
        if (n not in visited):
            find_min_green(n, node, previous, level + 1,
                           min_charge, bubble, visited)


def get_min_edge_and_epsilon(edges, flowers, matching, vertex_barbels,
                             blocking_edges, hung_trees, barbels):
    min_e = float('inf')
    min_edge = None
    opt = {'action': None}  # action and other fields goes here
    for edge, cost in edges.items():
        if (edge in matching or edge in blocking_edges):
            continue
        u, v = edge
        e = 0

        # count actual used edge capacity
        edge_border_charge = 0
        for f in flowers:
            # 1st blue bubble for edge
            if (f.vertex == u and f.color == 'blue'):
                e += f.charge
            # 2nd blue bubble for edge
            elif (f.vertex == v and f.color == 'blue'):
                e += f.charge
            # green bubble for which edge is in edge border
            elif (f.color == 'green'):
                edge_border_charge += get_edge_border_charge(f, u, v)
        e += edge_border_charge
        e = (cost - e)

        chosen = False

        # P1 green flower divided
        min_green = float('inf')
        tree = None
        final_bubble = None
        final_prev = None
        for t in hung_trees:
            bubble = [None]
            previous = [None]
            min_charge = [float('inf')]
            find_min_green(t.root, None, previous, 0, min_charge,
                           bubble, {})
            if (bubble[0] and previous[0] and min_charge[0] < min_green):
                min_green = min_charge[0]
                tree = t
                final_bubble = bubble[0]
                final_prev = previous[0]
        if (min_green < min_e and min_green >= 0):
            min_e = min_green
            min_edge = edge
            opt = {'action': P1, 't': tree, 'bubble': final_bubble,
                   'prev': final_prev}

        # P2 Tree and barbel
        if (not chosen):
            tree_flower = None
            barbel_flower = None  # barbel node to connect
            barbel = None  # barbel tuple
            barbel_vertex = None
            tree = None
            p2 = True

            # find flower in tree
            for t in hung_trees:
                v1 = get_outer_flower(t.root, u, {})
                v2 = get_outer_flower(t.root, v, {})

                if (v1 or v2):
                    tree = t
                    if (tree_flower):
                        p2 = False
                    if (v1):
                        tree_flower = v1
                        barbel_vertex = v
                    else:
                        tree_flower = v2
                        barbel_vertex = u
                if (v1 and v2):
                    p2 = False

            if (tree_flower and p2 and is_even(tree.root, tree_flower, 0, {})):
                # find posible barbel flower
                barbel_flower = get_flower(blue_flowers, barbel_vertex)
                if (not barbel_flower.is_outer):
                    barbel_flower = barbel_flower.outer

                # check if really is in some barbel
                for b in barbels:
                    if (b[0] is barbel_flower):
                        barbel = b
                    elif (b[1] is barbel_flower):
                        barbel = b
                if (barbel and e < min_e and e >= 0):
                    min_e = e
                    chosen = True
                    min_edge = edge
                    opt = {'action': P2, 'barbel': barbel}

        # P3 flowers in same tree
        if (not chosen):
            for t in hung_trees:
                v1 = get_outer_flower(t.root, u, {})
                v2 = get_outer_flower(t.root, v, {})
                if (v1 and v2):
                    even1 = is_even(t.root, v1, 0, {})
                    even2 = is_even(t.root, v2, 0, {})
                    if (even1 and even2):
                        chosen = True
                        if ((e / 2) < min_e and (e / 2) >= 0):
                            chosen = True
                            min_e = e / 2
                            min_edge = edge
                            opt = {'action': P3, 'v1': v1, 'v2': v2, 't': t}
                            break

        # P4 flowers in distinct trees
        if (not chosen):
            v1 = None
            v2 = None
            t1 = None
            t2 = None
            for t in hung_trees:
                v1_t = get_outer_flower(t.root, u, {})
                v2_t = get_outer_flower(t.root, v, {})

                if (v1_t):
                    v1 = v1_t
                    t1 = t
                if (v2_t):
                    v2 = v2_t
                    t2 = t
                if (v1 and v2):
                    even1 = is_even(t1.root, v1, 0, {})
                    even2 = is_even(t2.root, v2, 0, {})
                    if (even1 and even2):
                        chosen = True
                        if ((e / 2) < min_e and (e / 2) >= 0):
                            chosen = True
                            min_e = e / 2
                            min_edge = edge
                            opt = {'action': P4, 'v1': v1, 'v2': v2, 't1': t1,
                                   't2': t2}
                            break

    return (min_edge, min_e, opt)


def get_path(current, to, nodes, visited):
    '''
    Get path from one flower to anoter containing from
    outer flowers. Path is stored in 'nodes' and mutated
    during recursion.
    '''
    visited[current] = 1
    nodes.append(current)
    if (current is to):
        return nodes
    for n in current.get_next():
        if (n not in visited):
            res = get_path(n, to, nodes, visited)
            if (res):
                return res
    nodes.pop()


def get_full_inner_path(current, to, children, nodes, visited):
    visited[current] = 1
    nodes.append(current)
    if (current is to and len(nodes) > 1):
        return nodes
    for n in current.get_next():
        if (n in children and (n not in visited or
                               (len(nodes) >= 3 and
                                n is to))):
            res = get_full_inner_path(n, to, children, nodes, visited)
            if (res):
                return res
    nodes.pop()


def get_alt_path(current, to, nodes, seen, level, matching, blocking_edges):
    '''
    Get path from one blue flower to anoter blue flower
    containing from blue flowers. Edges on path are alternating.
    Path is stored in 'nodes' and mutated
    during recursion.
    level0 = next has to be barbel
    level1 = next has to be blocking edge
    '''
    nodes.append(current)
    if (current is to):
        return nodes
    for n in current.next:
        go = False
        if (level % 2 == 0):
            if ((n.vertex, current.vertex) in matching):
                go = True
        else:
            if ((n.vertex, current.vertex) in blocking_edges):
                go = True
        if (go and n not in seen):
            seen.append(n)
            res = get_alt_path(n, to, nodes, seen, level + 1, matching,
                               blocking_edges)
            if (res):
                return res
    nodes.pop()


def in_alt_path(node, alt_path):
    stack = copy.copy(node.flowers)
    # blue flower
    if (not stack):
        if (node in alt_path):
            return True
    else:
        while(len(stack)):
            last = stack.pop()
            if (last.color == 'green'):
                stack += last.flowers
            if (last.color == 'blue' and last in alt_path):
                return True
    return False


def split_tree_to_barbels(node, alt_path, level, barbels,
                          prev, visited, blocking_edges):
    visited[node] = 1
    if (level % 2 == 1):
        if (in_alt_path(node, alt_path)):
            barbels[(node, prev)] = 1
            barbels[(prev, node)] = 1
            # change stems
            b1, b2 = get_connection(node, prev)
            set_new_stems(node, b1)
            set_new_stems(prev, b2)
        else:
            b1, b2 = get_connection(node, prev)
            b1.next.remove(b2)
            b2.next.remove(b1)

            blocking_edges.pop(
                (b1.vertex, b2.vertex), None)
            blocking_edges.pop(
                (b2.vertex, b1.vertex), None)
    elif (level % 2 == 0 and prev is not None):
        if (not in_alt_path(node, alt_path)):
            barbels[(node, prev)] = 1
            barbels[(prev, node)] = 1
            # change stems
            b1, b2 = get_connection(node, prev)
            set_new_stems(node, b1)
            set_new_stems(prev, b2)
        else:
            b1, b2 = get_connection(node, prev)
            b1.next.remove(b2)
            b2.next.remove(b1)

            blocking_edges.pop(
                (b1.vertex, b2.vertex), None)
            blocking_edges.pop(
                (b2.vertex, b1.vertex), None)
    for n in node.get_next():
        if (n not in visited):
            split_tree_to_barbels(
                n, alt_path, level + 1, barbels, node,
                visited, blocking_edges)


def all_next_visited(blue_flower, visited):
    for n in blue_flower.next:
        if (n not in visited):
            return True
    return False


def is_complete(vertices, vertex_barbels):
    for v in vertices.keys():
        if (v not in vertex_barbels):
            return False
    return True


def get_connection(_from, _to):
    '''
    For two flowers return two blue flowers which connects them.
    '''
    from_b_flowers = _from.get_all_blue_flowers()
    to_b_flowers = _to.get_all_blue_flowers()
    b1 = None
    b2 = None
    for fb in from_b_flowers:
        for fn in fb.next:
            if (fn in to_b_flowers):
                b1 = fb
                b2 = fn
                break
        if (b1 and b2):
            break
    return (b1, b2)


if __name__ == '__main__':
    n_vertices = 0
    n_edges = 0
    no_solution = False

    matching = {}
    vertex_barbels = {}
    blocking_edges = {}
    barbels = {}
    vertices = {}
    flowers = []
    edges = {}
    hung_trees = []
    blue_flowers = {}

    f_name = './inputBig1.txt'
    with open(f_name) as f:
        striped = [line.rstrip() for line in f]
        for index, line in enumerate(striped):
            splited = [int(i) for i in line.split(' ')]
            if (index == 0):
                n_vertices = splited[0]
                n_edges = splited[1]
            else:
                if (splited[0] not in vertices):
                    vertices[splited[0]] = 1
                if (splited[1] not in vertices):
                    vertices[splited[1]] = 1
                edges[(splited[0], splited[1])] = splited[2]

    # Create empty blue bubble flower for every vertex
    for v in vertices.keys():
        f = Flower(None, None, 0, 'blue', v)
        flowers.append(f)
        blue_flowers[v] = f
        t = HungTree([f])
        hung_trees.append(t)

    while (not is_complete(vertices, vertex_barbels)):
        min_edge, eps, opt = get_min_edge_and_epsilon(edges, flowers,
                                                      matching,
                                                      vertex_barbels,
                                                      blocking_edges,
                                                      hung_trees,
                                                      barbels)

        add_charge(flowers, vertex_barbels, eps, hung_trees)

        # print(min_edge, eps, opt['action'])

        if (opt['action'] == P1):
            tree = opt['t']  # tree of current bubble
            bubble = opt['bubble']  # green bubble
            prev = opt['prev']  # previous bubble in tree

            for f in bubble.flowers:
                connection = get_connection(f, prev)

                # find flower in bubble from which we can access prev flower
                if (connection[0] is not None and connection[1] is not None):
                    _from = bubble.stem

                    # set outer flags
                    children = {}  # children of green bubble
                    for b in bubble.flowers:
                        children[b] = 1
                        b.is_outer = True
                        b.outer = None
                        if (b.flowers):
                            set_outer_flags(b.flowers, b)
                    flowers.remove(bubble)

                    if (not _from.is_outer):
                        _from = _from.outer

                    # path containing from all children of green bubble
                    full_path = []
                    get_full_inner_path(_from, _from, children, full_path, {})

                    # path from green bubble stem to flower which points
                    # to previous tree node
                    path = []
                    get_path(_from, f, path, {})

                    d_path = {}  # use dict to access elements quicker
                    for p in path:
                        d_path[p] = 1

                    # complementary path
                    comp_path = copy.copy(full_path)
                    for p in full_path:
                        if (p is not _from and p is not f):
                            if (p in d_path):
                                comp_path.remove(p)

                    if (len(path) > 1):
                        comp_path.pop()

                    # if complementary path was created in wrong direction
                    # need reverse action
                    if (comp_path[1] is f and len(comp_path) > 2):
                        temp = comp_path[1:]
                        temp.reverse()
                        comp_path = [comp_path[0]] + temp

                    tree_path = []  # path to retain in tree (odd)
                    barbels_path = []  # path to break to barbels (even)

                    # set odd resp. even path
                    if (len(path) % 2 == 0):
                        barbels_path = path
                        tree_path = comp_path
                    else:
                        barbels_path = comp_path
                        tree_path = path

                    # break barbels_path to barbels
                    for index in range(len(barbels_path)):
                        if (index > 0):
                            if (index % 2 == 1):
                                v1 = barbels_path[index]
                                v2 = barbels_path[index - 1]
                                b1, b2 = get_connection(v1, v2)
                                b1.next.remove(b2)
                                b2.next.remove(b1)
                                barbels[(v1, v2)] = 1
                                barbels[(v2, v1)] = 1

                                blocking_edges.pop(
                                    (b1.vertex, b2.vertex), None)
                                blocking_edges.pop(
                                    (b2.vertex, b1.vertex), None)
                    break

        elif (opt['action'] == P2):
            u, v = min_edge
            barbel = opt['barbel']  # tuple of flowers

            # remove flowers from barbels
            barbels.pop(barbel, None)
            barbels.pop(tuple(reversed(barbel)), None)

            blocking_edges[(u, v)] = 1
            blocking_edges[(v, u)] = 1

            # connect blue flowers
            b1 = get_flower(blue_flowers, u)
            b2 = get_flower(blue_flowers, v)
            b1.next.append(b2)
            b2.next.append(b1)

        elif (opt['action'] == P3):
            u, v = min_edge
            v1 = opt['v1']  # first vertex of last edge in cycle
            v2 = opt['v2']  # second vertex of last edge in cycle
            t = opt['t']  # tree in which cycle happened
            path1 = []  # path from root to v1
            path2 = []  # path from root to v2
            get_path(t.root, v1, path1, {})  # fill path1
            get_path(t.root, v2, path2, {})  # fill path2
            path1.reverse()

            path2_d = {}  # store in dict to access quicker
            for p2 in path2:
                path2_d[p2] = 1

            # find least common ancestor
            lca = None

            for p1 in path1:
                if (p1 in path2_d):
                    lca = p1
                    break

            path1 = []  # path from lca to v1
            path2 = []  # path from lca to v2
            get_path(lca, v1, path1, {})
            get_path(lca, v2, path2, {})

            b1 = get_flower(blue_flowers, u)
            b2 = get_flower(blue_flowers, v)
            b1.next.append(b2)
            b2.next.append(b1)

            path2.remove(lca)  # remove lca from second list
            inner_flowers = path1 + path2

            f = Flower(inner_flowers, lca.stem, 0, 'green')

            # If LCA flower was root in tree we have no set new root.
            # Otherwise there is no need to change other pointers.
            if (t.root is lca):
                t.root = f  # on root level

            set_outer_flags(inner_flowers, f)
            flowers.append(f)
            blocking_edges[(u, v)] = 1  # add blocking edge
            blocking_edges[(v, u)] = 1  # add blocking edge

        elif (opt['action'] == P4):
            v1 = opt['v1']
            v2 = opt['v2']
            t1 = opt['t1']
            t2 = opt['t2']

            u, v = min_edge
            b1 = get_flower(blue_flowers, u)
            b2 = get_flower(blue_flowers, v)

            b1.next.append(b2)
            b2.next.append(b1)

            # find alternating path
            alt_path1 = []
            alt_path2 = []
            stem_t1 = t1.root.stem
            stem_t2 = t2.root.stem
            get_alt_path(b1, stem_t1, alt_path1, [], 0, matching,
                         blocking_edges)
            get_alt_path(b2, stem_t2, alt_path2, [], 0, matching,
                         blocking_edges)
            alt_path1.reverse()
            alt_path = alt_path1 + alt_path2

            # swap barbels and blocking edges on alternating path
            for index in range(len(alt_path)):
                if (index < len(alt_path) - 1):
                    # get vertex values to remove from barbel/blocking edges
                    u_value = alt_path[index].vertex
                    v_value = alt_path[index + 1].vertex

                    # new edge is always barbel
                    if (u_value == b1.vertex and v_value == b2.vertex):
                        matching[(u_value, v_value)] = 1
                        matching[(v_value, u_value)] = 1
                        vertex_barbels[u_value] = 1
                        vertex_barbels[v_value] = 1

                    # remove from matching add to blocking edges
                    elif ((u_value, v_value) in matching or
                            (v_value, u_value) in matching):
                        matching.pop((u_value, v_value), None)
                        matching.pop((v_value, u_value), None)

                        # add both direction into blocking edges
                        blocking_edges[(u_value, v_value)] = 1
                        blocking_edges[(v_value, u_value)] = 1

                    # remove from blocking edges add to matching
                    elif ((u_value, v_value) in blocking_edges or
                            (v_value, u_value) in blocking_edges):
                        blocking_edges.pop((u_value, v_value), None)
                        blocking_edges.pop((v_value, u_value), None)
                        matching[(u_value, v_value)] = 1
                        matching[(v_value, u_value)] = 1
                        vertex_barbels[u_value] = 1
                        vertex_barbels[v_value] = 1

            alt_path_d = {}  # store in dict to access quicker
            for ap in alt_path:
                alt_path_d[ap] = 1

            # remove connection to split trees separately
            b1.next.remove(b2)
            b2.next.remove(b1)

            split_tree_to_barbels(t1.root, alt_path_d, 0,
                                  barbels, None, {}, blocking_edges)
            split_tree_to_barbels(t2.root, alt_path_d, 0,
                                  barbels, None, {}, blocking_edges)

            # add connection again
            b1.next.append(b2)
            b2.next.append(b1)

            # create barbel from newly connected flowers
            barbels[(v1, v2)] = 1
            barbels[(v2, v1)] = 1

            # remove trees from hung_tress
            hung_trees.remove(t1)
            hung_trees.remove(t2)

        else:
            no_solution = True
            break

        # print('barbels', barbels)
        # print('matching', matching)
        # print('blocking edges', blocking_edges)
        # print('hung tress count', len(hung_trees))

    if (no_solution):
        print('No solution')
    else:
        matching_cost = 0
        final_matching = []
        print('Edges in matching')
        for m in matching:
            if (m[0] < m[1]):
                final_matching.append((m[0], m[1]))
                matching_cost += edges[(m[0], m[1])]
                print(m[0], m[1])
        print('Matching cost')
        print(matching_cost)
